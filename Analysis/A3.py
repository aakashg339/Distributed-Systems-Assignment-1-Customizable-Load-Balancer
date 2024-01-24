import requests
import helper

# Test adding Endpoint 
add_response = requests.post('http://localhost:5000/add', json={"n": 1, "hostnames": ["server4"]})
print(add_response.json())

# Testing replicas Endpoint 
rep_response = requests.get('http://localhost:5000/rep') 
print(rep_response.json())

remove_response = requests.delete('http://localhost:5000/rm', json={"n": 1, "hostnames": ["server1"]})
print(remove_response.json())

# server failure by stopping a Docker container and observe the load balancer's response
print("Before Failure : ")
rep_response = requests.get('http://localhost:5000/rep') 
print(rep_response.json())
helper.dropServer("server1")
print("After Failure : ")
rep_response = requests.get('http://localhost:5000/rep') 
print(rep_response.json())
