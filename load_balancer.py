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

N = 3
currentNumberofServers = 0
serverName = []
servers = {}
virtualServers = 9
slotsInHashMap = 512
consistentHashMap = ConsistentHashmapImpl([], virtualServers, slotsInHashMap)
counter = 1
max_servers = slotsInHashMap//virtualServers
max_request = 100000
server_hash = {}
server_ids = [0] * max_servers
logging.basicConfig(level=logging.DEBUG)

def getServerID():
    for i in range(1, max_servers + 1): 
        if server_ids[i] == 0: 
            server_ids[i] = 1
            return i
    return -1

def removeServer(i):
    server_ids[i] = 0

# This will return the status of the servers maintained by the load balancer
@app.route('/rep', methods=['GET'])
def get_replicas_status(): 
    global replicas
    replicas = consistentHashMap.getServers()
    response_json = {
        "message" : { 
            "N" : len(replicas), 
            "replicas" : replicas 
        },
        "status" : "successful"
    }
    return jsonify(response_json), 200


# This will add new server instances in the load balancer
@app.route('/add', methods=['POST'])
def add_replicas():
    global replicas
    payload = request.get_json()
    n = payload.get('n')
    hostnames = payload.get('hostnames', [])

    # Sanity checks ---------------------------------------------------------------------
    if len(hostnames) > n : 
        response_json = {
            "message": {
                "<Error> Length of hostname list is more than newly added instances"
            },
            "status": "failure"
        }
        return jsonify(response_json), 400
    
    # TODO : Will add set based check, if 2 server names are same 



    # Update replicas based on consistent hashing logic
    # TODO : Will Complete this after @Soham Completes the Hash-Map Function 
    global currentNumberofServers
    for id in hostnames:
        x = getServerID()
        helper.createServer(x)
        servers[x] = f"http://server{x}:5000/"
        serverName.append(id)
        consistentHashMap.addServer(x)
        server_hash[id] = [id, str(x)]
        currentNumberofServers+=1

    replicas = consistentHashMap.getServers() 
    response_json = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response_json), 200


@app.route('/rm', methods = ['DELETE'])
def remove_server():
    global replicas
    replicas = consistentHashMap.getServers()
    payload = request.get_json()
    n = payload.get('n')
    hostnames = payload.get('hostnames', [])

    # Sanity Checks ---------------------------------------------------------------------
    if len(hostnames)>n: 
        response_json = {
            "message": {
                "<Error> Length of hostname list is more than removable instances"
            },
            "status": "failure"
        }
        return jsonify(response_json), 400

    for id in hostnames: 
        if id not in replicas:
            response_json = {
                "message" : {
                    "msg": "<Error> Hostname mentioned is not present in the server list"
                },
                "status" : "failure" 
            }
            return jsonify(response_json), 400
        
    
    # TODO : Should we allow to remove 'all' servers ? 
    if n > len(replicas) : 
        response_json = {
            "message": {
                "<Error> No of servers to be removed is more than actual count of servers"
            },
            "status": "failure"
        }
        return jsonify(response_json), 400
    
    # handling remove servers 
    global currentNumberofServers
    for id in hostnames :
        print("^^^^^" + id)
        os.system(f'docker stop server{server_hash[id][1]} && docker rm server{server_hash[id][1]}')
        consistentHashMap.removeServer(int(server_hash[id][1]),(server_hash[id][0]) )
        del servers[int(server_hash[id][1])]
        del server_hash[id]
        currentNumberofServers-=1
        n-=1
    
    # If any the spcified hostnames are less the number of containers to be actually removed 
    while n!=0 :
        id = consistentHashMap.getRandomServerId()
        os.system(f'docker stop server{server_hash[id]} && docker rm {server_hash[id]}')
        consistentHashMap.removeServer(id)
        del servers[int(server_hash[id][1])]
        del server_hash[id]
        currentNumberofServers-=1
        n-=1

    rr = consistentHashMap.getServers()
    print(servers)
    response_json = {
        "message" : {
            "replicas" : rr
        },
        "status" : "success" 
    }
    return jsonify(response_json), 200
    
def get_container_ip(container_name):
    # Get the IP address of the container
    return os.popen(f'docker inspect -f "{{{{.NetworkSettings.Networks.my_network.IPAddress}}}}" {container_name}').read().strip()

@app.route('/<path>', methods=['GET'])
def route_to_replica(path):
    available_servers = list(servers.keys())
    counter = available_servers[(random.randint(0,currentNumberofServers-1))]
    container_name = f'server{counter}'
    container_id = consistentHashMap.getContainerID(counter)
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
    for i in range(1, 4):
        x = getServerID()
        helper.createServer(x) 
        consistentHashMap.addServer(x, f"server{x}")
        servers[i] = f"http://server{x}:5000/"
        serverName.append(f"server{x}")
        print(consistentHashMap.getServers())
        server_hash["server"+str(x)] = ["server"+str(x), str(x)]
        currentNumberofServers+=1

    logging.info("***********************************")
    logging.info(os.popen(f"docker ps -a").read())
    app.run(host="0.0.0.0", port=5000, threaded=True)