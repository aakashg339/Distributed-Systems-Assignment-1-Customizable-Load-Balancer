# Implementation of the server

from flask import Flask
import os

#creating the Flask class object
app = Flask(__name__)

# Server endpoint for requests at http://localhost:5000/home, methond=GET
@app.route('/home', methods = ['GET'])
def home():
    # Server ID taking from the environment variable named SERVER_ID
    serverID = os.environ.get('SERVER_ID')

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

# Server endpoints for all other requests. Kind of error handler
@app.route('/', defaults={'path': ''}, methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
@app.route('/<path:path>', methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def invalidUrlHandler(path):
    # Returning an error message stating the valid endpoints
    errorMessage = {"message": "Invalid Endpoint",
                    "Valid Endpoints": ["/home method='GET'", "/heartbeat method='GET'"],
                    "status": "Unsuccessfull"}
    
    # Returning the JSON object along with the status code 404
    return errorMessage, 404
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)