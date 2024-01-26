import asyncio
import aiohttp
import requests
import matplotlib.pyplot as plt
import statistics
import Analysis.analysis1 as analysis1

async def send_request(session, url):
    async with session.get(url) as response:
        return await response.text()

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
total_requests = 100

# Number of iterations
num_iterations = 5

# Results for each iteration
iteration_results = []

# Run the test for each N = number of servers
for n in range(1, 6):
    print(f"Testing with {n+1} servers...")
    if n >= 2:
        print(requests.post('http://localhost:5000/add', json={"n": 1, "hostnames": [Server_Ids[n-2]]}).text)
        print(requests.get('http://localhost:5000/serverno').text)
    
    analysis1.runner()
   