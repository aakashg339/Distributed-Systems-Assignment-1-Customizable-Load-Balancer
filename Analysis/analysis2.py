import asyncio
import aiohttp
import requests
import matplotlib.pyplot as plt
import statistics

async def send_request(session, url):
    async with session.get(url) as response:
        return await response.text()

def parse_server_id(response):
    # Your parsing logic goes here, modify as needed
    # Example: Extract the server ID from a response string
    ser = ""
    cond = False
    for i in response:
        if i == '[':
            cond = True
            continue
        elif i == ']':
            break
        if cond:
            ser += i
    if len(ser) != 0:
        return ser
    else:
        return None

async def test_load_distribution(server_count, total_requests):
    url = "http://localhost:5000/home"
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(total_requests):
            task = asyncio.ensure_future(send_request(session, url))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        server_counts = {}
        for response in responses:
            server_id = parse_server_id(response)
            server_counts[server_id] = server_counts.get(server_id, 0) + 1

        return server_counts

# Server IDs
Server_Ids = ["S1", "S2", "S3", "S4"]

# Number of requests for each run
total_requests = 10000

# Dictionary to store the sum of requests handled by each server across iterations
total_requests_by_server = {}
total_requests_by_server_counts = {}
# Run the test for each N = number of servers
for n in range(1, 6):
    print(f"Testing with {n+1} servers...")
    if n >= 2:
        print(requests.post('http://localhost:5000/add', json={"n": 1, "hostnames": [Server_Ids[n-2]]}).text)
        print(requests.get('http://localhost:5000/serverno').text)

    # Run the test and accumulate results for each server
    server_counts = asyncio.run(test_load_distribution(n, total_requests))
    
    # Accumulate the sum of requests handled by each server
    for server_id, count in server_counts.items():
        if server_id == None : 
            continue
        if server_id not in total_requests_by_server:
            total_requests_by_server[server_id] = 0
        total_requests_by_server[server_id] += count
    for k, v in total_requests_by_server.items():
        if k not in total_requests_by_server_counts: 
            total_requests_by_server_counts[k] = 0
        total_requests_by_server_counts[k]+=1

# Calculate the average load for each server

# average_loads = {server_id: total / (n + 1) for server_id, total in total_requests_by_server.items()}
for k, v in total_requests_by_server.items(): 
    total_requests_by_server[k]/=total_requests_by_server_counts[k]

average_loads = total_requests_by_server
# Plotting the bar graph
plt.bar(average_loads.keys(), average_loads.values())
plt.xlabel('Server IDs')
plt.ylabel('Average Load per Server')
plt.title('Average Load per Server Across Iterations')
plt.show()


plt.plot(list(average_loads.keys()), list(average_loads.values()), marker='o', linestyle='-')
plt.xlabel('Server IDs')
plt.ylabel('Average Load per Server')
plt.title('Average Load per Server Across Iterations')
plt.grid(True)
plt.show()