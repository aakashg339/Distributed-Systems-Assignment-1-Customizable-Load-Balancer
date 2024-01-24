import requests

# Test adding and removing servers
add_response = requests.post('http://localhost:8000/add', json={"n": 1, "hostnames": ["Server4"]})
print(add_response.json())

remove_response = requests.delete('http://localhost:8000/rm', json={"n": 1, "hostnames": ["Server4"]})
print(remove_response.json())

# Simulate server failure by stopping a Docker container and observe the load balancer's response
