# Custom Load Balancer
<p align="center">
      <img src="images/overview.png" width="90%"/><br><strong>Fig.1: Overview</strong>
</p>

# Overview

t a load balancer that routes the requests coming from several clients asynchronously among several servers so that the load is nearly evenly distributed among them. In order to scale a particular service with increasing clients, load balancers are used to manage multiple replicas of the service to improve resource utilization and throughput. In the real world, there are various use cases of such constructs in distributed caching systems, distributed database management systems, network traffic systems, etc. To efficiently distribute the requests coming from the clients, a load balancer uses a consistent hashing data structure.The load balancer is exposed to the clients through the APIs shown in the diagram (details on the APIs are given further). There should always be N servers present to handle the requests. In the event of failure, new replicas of the server will be spawned by the load balancer to handle the requests.

# SERVER
A simple web server that accepts HTTP requests on port 5000 in the below endpoints.
### Endpoints

1. **Endpoint: /home (Method: GET)**
   - Returns a string with a unique identifier, distinguishing among replicated server containers.
   - Example Response JSON:
     ```json
     {
       "message": "Hello from Server: [ID]",
       "status": "successful"
     }
     ```
   - Response Code: 200

2. **Endpoint: /heartbeat (Method: GET)**
   - Sends heartbeat responses upon request. Used by the load balancer to identify container failures.
   - Example Response: [EMPTY]
   - Response Code: 200

## Dockerfile

To containerize the server as an image and make it deployable, a Dockerfile is provided. Note that containers can communicate via hostnames in a Docker network, utilizing Docker's built-in DNS service for hostname resolution within the same network.

### Instructions

### Usage

```bash
# Build Docker image
docker build -t server-image .

# Run Docker container
docker run -p 5000:5000 --name server-container server-image
```

# Consistent Hash Map Implementation


- **Number of Server Containers managed by the load balancer (N):** 3
- **Total number of slots in the consistent hash map (#slots):** 512
- **Number of virtual servers for each server container (K):** log(512) = 9
- **Hash function for request mapping H(i):** i^2 + 2i + 17
- **Hash function for virtual server mapping Φ(i, j):** i^2 + j^2 + 2j + 25

### Implementation Details

- Two client requests may be mapped to the same slot in the hash map. However, if there is a conflict between two server instances, apply Linear or Quadratic probing to find the next suitable slot.
- Server containers and virtual servers are distinct concepts. Server containers are the number of containers the load balancer manages to handle requests. A virtual server is a theoretical concept that repeats the location of server containers in the consistent hash, aiding better load distribution in case of failure. Virtual servers are not directly tied to the actual number of server containers.

### Hash Functions

1. **Request Mapping Hash Function (H(i)):** `i^2 + 2i + 17`
2. **Virtual Server Mapping Hash Function (Φ(i, j)):** `i^2 + j^2 + 2j + 25`

### Handling Conflicts

In case of conflicts between server instances, Quadratic probing is used to locate the next suitable slot in the hash map.

# Load-Balancer

# Analysis

For Running the LoadBalancer, in the root dorectory, run command : 
$ make start


Run : 
docker run -p 5000:5000 --privileged=true -v /var/run/docker.sock:/var/run/docker.sock --name Load_Balancer --network my_network -it loadbalancer
