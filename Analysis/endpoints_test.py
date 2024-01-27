import requests

# base URL for the load balancer
base_url = "http://localhost:5000"

# Endpoint 1: /rep (GET)
rep_endpoint_url = f"{base_url}/rep"
rep_response = requests.get(rep_endpoint_url)
print("Endpoint /rep:")
print("Response Code: ", rep_response.status_code)
print("Response JSON: ", rep_response.json())
print()

# Endpoint 2: /add (POST)
add_endpoint_url = f"{base_url}/add"
add_payload = {
    "n": 5,
    "hostnames": ["S5", "S4", "S10", "S11"]
}
add_response = requests.post(add_endpoint_url, json=add_payload)
print("Endpoint /add:")
print("Request Payload: ", add_payload)
print("Response Payload: ", add_response.json())
print()

# Endpoint 3: /rm (DELETE)
rm_endpoint_url = f"{base_url}/rm"
rm_payload = {
    "n": 3,
    "hostnames": ["S5", "S4"]
}
rm_response = requests.delete(rm_endpoint_url, json=rm_payload)
print("Endpoint /rm:")
print("Request Payload: ", rm_payload)
print("Response Payload : ",  rm_response.json())
print()

# Endpoint 4: /<path> (GET)
path_endpoint_url = f"{base_url}/home" 
path_response = requests.get(path_endpoint_url)
print("Endpoint /home:")
print("Request URL:", path_endpoint_url)
print("Response :", path_response.json())

