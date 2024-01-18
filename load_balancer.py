from flask import Flask, jsonify, request
import random
import json

app = Flask(__name__)

replicas = ["Server 1", "Server 2", "Server 3"]


# This will return the status of the servers maintained by the load balancer
@app.route('/rep', methods=['GET'])
def get_replicas_status(): 
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
    payload = request.get_json()
    n = payload.get('n')
    hostnames = payload.get('hostnames', [])

    # Sanity Checks ---------------------------------------------------------------------
    if len(hostnames) > n : 
        response_json = {
            "message": {
                "<Error> Length of hostname list is more than removable instances"
            },
            "status": "failure"
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


@app.route('/<path>', methods=['GET'])
def route_to_replica(path):
     # TODO : After Hash-Map is implemented 
    return "" , 400 



if __name__ =='__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)