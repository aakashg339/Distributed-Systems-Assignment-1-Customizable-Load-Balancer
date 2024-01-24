**Distributed Systems Assignment: Custom Load Balancer**
**Overview**

This assignment involves the design and implementation of a custom load balancer within a distributed system. The objective is to evenly distribute client requests across a set of server instances using consistent hashing. This project is crucial for understanding the principles behind request routing, load balancing, and the handling of server failures in distributed environments.
Environment Setup

    Programming Language: Python 3.8+
    Dependencies: Flask, hashlib, Docker
    Tools: Docker for containerization, Postman or curl for testing

**Getting Started**

Clone the repository and navigate into the project directory:

bash Command:
git clone <repository-url>
cd <project-directory>

Install the required Python dependencies:

bash Command:
pip3 install -r requirements.txt

Build and run the Docker containers for the servers:

bash Command
docker-compose up --build -d

**Task Breakdown**
**Task 1: Simple Web Server**

Implemented a basic Flask web server that listens on port 5000. The server has two endpoints:

    /: Returns a simple greeting.
    /heartbeat: Returns a 200 OK status to indicate the server is alive.

To run the server:

bash Command:
python server.py

**Task 2: Consistent Hashing**

Developed a consistent hashing module to distribute incoming requests evenly across the available servers. This module uses the MD5 hashing algorithm to ensure a uniform distribution of hash values.
Task 3: Load Balancer Implementation

The load balancer, built with Flask, routes incoming requests to the server instances based on the consistent hashing algorithm. It monitors server health through the /heartbeat endpoint and reroutes traffic in case of failures.

To start the load balancer:

bash Command:
python load_balancer.py

Task 4: Analysis and Testing

Conducted performance tests to evaluate the load balancer's efficiency in request distribution and failover mechanisms. The analysis includes response time measurements and server load distribution under various conditions.

**Testing**

Use Postman or curl to send requests to the load balancer and observe the routing of requests to different server instances.

Example curl request:

bash Command:
curl http://localhost:8000/
