import asyncio
import aiohttp
import requests
import matplotlib.pyplot as plt
import statistics
import analysis

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
            server_id = response.split()[-1]  # Extract server ID from response
            server_counts[server_id] = server_counts.get(server_id, 0) + 1

        return server_counts

# Server IDs
Server_Ids = ["S1", "S2", "S3", "S4"]

# Number of requests for each run
total_requests = 10

# Results for each server in each iteration
server_results = {Server_Ids[i]: [0]*(4-i) for i in range(len(Server_Ids))}

# Run the test for each N = number of servers
for n in range(1, 6):
    print(f"Testing with {n+1} servers...")
    if n >= 2:
        print(requests.post('http://localhost:5000/add', json={"n": 1, "hostnames": [Server_Ids[n-2]]}).text)
        print(requests.get('http://localhost:5000/serverno').text)


    # Run the test and accumulate results for each server
    server_counts = asyncio.run(test_load_distribution(n, total_requests))
    for response in server_counts:
        # Parse the response to get the server ID
        server_id = parse_server_id(response)

        # Debug print to check the extracted server ID
        print(f"Response: {response}, Extracted Server ID: {server_id}")

        # Append the count to the corresponding server's results
        if server_id is not None:
            if server_id not in server_results : 
                server_results[server_id] = [0]
            server_results[server_id].append(server_counts[response])
        else:
            print("Failed to extract server ID from response.")


# Calculate the average load for each server
average_loads = {server_id: statistics.mean(counts) for server_id, counts in server_results.items()}

# Plotting the line chart
plt.figure(figsize=(10, 6))
for server_id, avg_load in average_loads.items():
    plt.plot(range(1, 6), [avg_load] * 5, 'o-', label=f'Server {server_id}')

plt.xlabel('Number of Servers')
plt.ylabel('Average Load per Server')
plt.title('Average Load per Server for Different Server Counts')
plt.legend()
plt.grid(True)
plt.show()