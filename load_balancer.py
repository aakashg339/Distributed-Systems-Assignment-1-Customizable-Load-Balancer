from flask import Flask, jsonify, request
import os 
import logging 
import random
import requests
import json
import helper
from ConsistentHashmap import ConsistentHashmapImpl

app = Flask(__name__)

replicas = ["Server 1", "Server 2", "Server 3"]
# os.popen(f"docker build -t serverimage ./Server")

# NumberofServers = 3 
# serverName = ["S1", "S2", "S3"]
servers = {}
virtualServers = 9
slotsInHashMap = 512
consistentHashMap = ConsistentHashmapImpl(servers, virtualServers, slotsInHashMap)
counter = 1
max_servers = slotsInHashMap//virtualServers
max_request = 100000
server_ids = [0] * max_servers
logging.basicConfig(level=logging.DEBUG)

# def getServerID():
#     for i in range(1, max_servers + 1): 
#         if server_ids[i] == 0: 
#             server_ids[i] = 1
#             return i
#     return -1

# def removeServer(i):
#     server_ids[i] = 0

# This will return the status of the servers maintained by the load balancer
# @app.route('/rep', methods=['GET'])
# def get_replicas_status(): 
#     global replicas
#     replicas = consistentHashMap.getServers()
#     response_json = {
#         "message" : { 
#             "N" : len(replicas), 
#             "replicas" : replicas 
#         },
#         "status" : "successful"
#     }
#     return jsonify(response_json), 200


# # This will add new server instances in the load balancer
# @app.route('/add', methods=['POST'])
# def add_replicas():
#     global replicas
#     payload = request.get_json()
#     n = payload.get('n')
#     hostnames = payload.get('hostnames', [])

#     # Sanity checks ---------------------------------------------------------------------
#     if len(hostnames) > n : 
#         response_json = {
#             "message": {
#                 "<Error> Length of hostname list is more than newly added instances"
#             },
#             "status": "failure"
#         }
#         return jsonify(response_json), 400
    
#     # TODO : Will add set based check, if 2 server names are same 



#     # Update replicas based on consistent hashing logic
#     # TODO : Will Complete this after @Soham Completes the Hash-Map Function 
#     for id in hostnames:
#         res=helper.createServer(id)
#         if len(res) == 0:
#             print("Unable to start containerB")
#             return {
#                 "Message" : "Failed to spawn server", 
#                 "status": "failure"
#             } , 400 
#         consistentHashMap.addServer(id)
#     replicas = consistentHashMap.getServers() 
#     response_json = {
#         "message": {
#             "N": len(replicas),
#             "replicas": replicas
#         },
#         "status": "successful"
#     }
#     return jsonify(response_json), 200


# @app.route('/rm', methods = ['DELETE'])
# def remove_server():
#     global replicas
#     replicas = consistentHashMap.getServers()
#     payload = request.get_json()
#     n = payload.get('n')
#     hostnames = payload.get('hostnames', [])

#     # Sanity Checks ---------------------------------------------------------------------
#     if len(hostnames)>n: 
#         response_json = {
#             "message": {
#                 "<Error> Length of hostname list is more than removable instances"
#             },
#             "status": "failure"
#         }
#         return jsonify(response_json), 400

#     for id in hostnames: 
#         if id not in replicas:
#             response_json = {
#                 "message" : {
#                     "<Error> Hostname mentioned is not present in the server list"
#                 },
#                 "status" : "failure" 
#             }
#             return jsonify(response_json), 400
        
    
#     # TODO : Should we allow to remove 'all' servers ? 
#     if n > len(replicas) : 
#         response_json = {
#             "message": {
#                 "<Error> No of servers to be removed is more than actual count of servers"
#             },
#             "status": "failure"
#         }
#         return jsonify(response_json), 400
    
#     # handling remove servers 
#     for id in hostnames :
#         os.system(f'docker stop {id} && docker rm {id}')
#         consistentHashMap.removeServer(id)
#         n-=1
    
#     # If any the spcified hostnames are less the number of containers to be actually removed 
#     while n!=0 :
#         id = consistentHashMap.getRandomServerId()
#         os.system(f'docker stop {id} && docker rm {id}')
#         consistentHashMap.removeServer(id)
#         n-=1
def get_container_ip(container_name):
    # Get the IP address of the container
    return os.popen(f'docker inspect -f "{{{{.NetworkSettings.Networks.my_network.IPAddress}}}}" {container_name}').read().strip()

@app.route('/<path>', methods=['GET'])
def route_to_replica(path):
    global counter 
    counter = (counter + 1) % 3 + 1 
    container_name = f'server{counter}'
    
    # Get the IP address of the container
    container_ip = get_container_ip(container_name)
    server_url = f"http://{container_ip}:5000/{path}"
    
    logging.debug(f"Attempting to access container: {container_name} with IP: {container_ip}")
    
    try:
        response = requests.get(server_url)
        logging.debug(f"Response from container: {response.text}")
        return response.text, response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to {server_url}: {e}")
        return "Error connecting to replica", 500

if __name__ =='__main__':
    logging.info("***********************************")
    try:
        logging.info(os.popen(f"docker network create my_network").read())
    except:
        logging.info("Network my_network already exists.")
    
    for i in range(1, 4):  # Adjust the range to include 3 containers
        helper.createServer(i) 
        servers[i] = f"http://server{i}:5000/"
    
    logging.info("***********************************")
    logging.info(os.popen(f"docker ps -a").read())
    app.run(host="0.0.0.0", port=5000, threaded=True)