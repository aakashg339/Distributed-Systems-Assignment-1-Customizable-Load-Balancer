from flask import Flask, jsonify, request
import os 
import logging 
import random
import requests
import json
import threading
import time
import helper
from ConsistentHashmap import ConsistentHashmapImpl

app = Flask(__name__)

replicas = []
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


def check_server_health(server_url):
    try:
        response = requests.get(f"{server_url}/heartbeat", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def health_check():
    global servers, currentNumberofServers
    while True:
        time.sleep(10)
        for server_name, server_url in servers.items():
            if not check_server_health(server_url[1]):
                id = servers[server_name][0]
                logging.debug(f"Server : {server_name} is down. Removing from the pool.")
                os.system(f'docker stop server{server_name} && docker rm {server_name}')
                del servers[server_name]
                del server_hash[id]
                removeServer(id)
                consistentHashMap.removeServer(id, server_name)
                currentNumberofServers-=1

        # Check if the number of running servers is less than 3
        while currentNumberofServers < 3:
            x = getServerID()
            name = f"server{x}"
            logging.debug(f"Creating new Server :{name}")
            helper.createServer(x, name)
            consistentHashMap.addServer(x, name)
            servers[name] = [x, f"http://{get_container_ip(name)}:5000/"]
            server_hash[x] = name
            currentNumberofServers+=1


def start_health_check_thread():
    health_check_thread = threading.Thread(target=health_check)
    health_check_thread.daemon = True
    health_check_thread.start()


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
    
    # Set based check, if 2 server names are same
    duplicates = False
    for name in hostnames :
        if name in list(servers.keys()):
            duplicates = True
            break
    if len(set(hostnames))<n:
        duplicates = True
    if duplicates == True:
        return {
            "message": {
                "<Error> duplicate hostnames"
            },
            "status": "failure"
        }, 400
        

    # Update replicas based on consistent hashing logic

    global currentNumberofServers
    for id in hostnames:
        x = getServerID()
        name = id
        helper.createServer(x, name)
        consistentHashMap.addServer(x, name)
        servers[name] = [x, f"http://{get_container_ip(name)}:5000/"]
        server_hash[x] = name
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
    print("****************************************************")
    print(hostnames)
    print(replicas)
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
    for name in hostnames :
        os.system(f'docker stop server{name} && docker rm server{name}')
        consistentHashMap.removeServer(servers[name][0], name)
        del server_hash[servers[name][0]]
        removeServer(servers[name][0])
        del servers[name]
        currentNumberofServers-=1
        n-=1
    
    # If any the spcified hostnames are less the number of containers to be actually removed 
    while n!=0 :
        name = server_hash[consistentHashMap.getRandomServerId()]
        os.system(f'docker stop server{name} && docker rm server{name}')
        consistentHashMap.removeServer(servers[name][0], name)
        del server_hash[servers[name][0]]
        removeServer(servers[name][0])
        del servers[name]
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
    global counter 
    counter = (counter+1)%max_request
    container_id = consistentHashMap.getContainerID(counter)
    print(f"$$$$$$$$$$$$$$$$$$ {container_id}")
    container_name = server_hash[container_id]
    container_ip = get_container_ip(container_name)
    server_url = servers[container_name][1]+str(path)
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
    logging.debug(os.popen("docker rm -f  $(docker ps -aq)").read())
    try:
        logging.info(os.popen(f"docker network create my_network").read())
    except:
        logging.info("Network my_network already exists.")
    for i in range(1, 4):
        x = getServerID()
        name = f"server{x}"
        helper.createServer(x, name)
        consistentHashMap.addServer(x, name)
        servers[name] = [x, f"http://{get_container_ip(name)}:5000/"]
        server_hash[x] = name
        currentNumberofServers+=1

    logging.info("***********************************")
    logging.info(os.popen(f"docker ps -a").read())
    start_health_check_thread()
    app.run(host="0.0.0.0", port=5000, threaded=True)