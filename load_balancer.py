from flask import Flask, jsonify, request
import os 
import random
import requests
import json
import helper
from ConsistentHashmap import ConsistentHashmapImpl

app = Flask(__name__)

replicas = ["Server 1", "Server 2", "Server 3"]

# requestId = 0 
# request_threshold = 10000000
# # Testing the Consistent Hash Map Implementation.
# servers = [1, 2, 3]
# requestIds = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# virtualServers = 9
# slotsInHashMap = 512
# consistentHashMap = ConsistentHashmapImpl(servers, virtualServers, slotsInHashMap)
# for serverId in servers:
#     consistentHashMap.addServer(serverId)

# print(consistentHashmapImpl.hashmap)
# print(consistentHashmapImpl.sorted_keys)

# consistentHashmapImpl.removeServer(2)
# print(consistentHashmapImpl.hashmap)
# print(consistentHashmapImpl.sorted_keys)

# for requestId in requestIds:
#     consistentHashMap.addRequest(requestId)

# for requestId in requestIds:
#     consistentHashMap.addRequest(requestId)

# # print(consistentHashMap.hashmap)
# for k, v in consistentHashMap.hashmap.items(): 
#     print(f"{k} - {v}")

# print()
# print()
# consistentHashMap.removeRequest(2)
# for k, v in consistentHashMap.hashmap.items(): 
#     print(f"{k} - {v}")



SERVERS = {
    1: "http://server1:5000",
    2: "http://server2:5000",
    3: "http://server3:5000",
}

servers = list(SERVERS.keys())
virtualServers = 9
slotsInHashMap = 512
consistentHashMap = ConsistentHashmapImpl(servers, virtualServers, slotsInHashMap)
for serverId in servers:
    consistentHashMap.addServer(serverId)
    print("Server create Status : " + str(helper.createServer(serverId)))




# # This will return the status of the servers maintained by the load balancer
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
#     if len(hostnames) > n : 
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
#         os.system(f'sudo docker stop {id} && sudo docker rm {id}')
#         consistentHashMap.removeServer(id)
#         n-=1
    
#     # If any the spcified hostnames are less the number of containers to be actually removed 
#     while n!=0 :
#         id = consistentHashMap.getRandomServerId()
#         os.system(f'sudo docker stop {id} && sudo docker rm {id}')
#         consistentHashMap.removeServer(id)
#         n-=1

@app.route('/<path>', methods=['GET'])
def route_to_replica(path):
    hashed_value = helper.hash_function(path)
    server_keys = list(SERVERS.keys())
    selected_server = server_keys[hashed_value % len(server_keys)]
    server_url = servers[selected_server] + f'/home'
    response = requests.get(server_url)
    return response.text, response.status_code

if __name__ =='__main__':
    # servers = list(SERVERS.keys())
    # virtualServers = 9
    # slotsInHashMap = 512
    # consistentHashMap = ConsistentHashmapImpl(servers, virtualServers, slotsInHashMap)
    # for serverId in servers:
    #     consistentHashMap.addServer(serverId)
    #     print("Server create Status : " + str(helper.createServer(serverId)))
    app.run(host="0.0.0.0", port=5000, debug = True)