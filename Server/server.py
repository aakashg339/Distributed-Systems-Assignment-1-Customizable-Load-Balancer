# Implementation of the server

from flask import Flask  

#creating the Flask class object
app = Flask(__name__)

# Server endpoint for requests at http://localhost:5000/home, methond=GET
@app.route('/home', methods = ['GET'])
def home():
    # Server ID (will me modified later to be used from environment variables)
    serverID = 23

    # Dictionary to return as a JSON object
    serverHomeMessage =  {"message": "Hello from Server: [" + str(serverID) + "]",
                          "status": "successfull"}

    # Returning the JSON object along with the status code 200
    return serverHomeMessage, 200

# Server endpoint for requests at http://localhost:5000//heartbeat, method=GET
@app.route('/heartbeat', methods = ['GET'])
def heartbeat():
    # Returning empty response along with status code 200
    return "", 200
    
if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)