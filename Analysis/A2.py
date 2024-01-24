import asyncio
import aiohttp
import requests
import matplotlib.pyplot as plt
import statistics

async def send_request(session, url):
    async with session.get(url) as response:
        return await response.text()


async def test_load_distribution(server_count):
    url = "http://localhost:5000/home"
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(10000):
            task = asyncio.ensure_future(send_request(session, url))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        server_counts = {}
        for response in responses:
            server_id = response.split()[-1]  # Extract server ID from response
            server_counts[server_id] = server_counts.get(server_id, 0) + 1

        return server_counts


server_ids = ["S1", "S2", "S3"]
for n in range(3, 5):
    print(f"Testing with {n} servers...")

    if n > 3:
        requests.post('http://localhost:5000/add', json={"n": n-3, "hostnames": server_ids[:n-3]})

    results = []
    for _ in range(2):  # Run 10 times and average the results
        server_counts = asyncio.run(test_load_distribution(n))
        results.append(server_counts)

    # Calculate average load for each server
    average_loads = {}
    for server_id in server_ids[:n]:
        loads = [result.get(server_id, 0) for result in results]
        average_load = statistics.mean(loads)
        average_loads[server_id] = average_load

    # Print and plot the results
    print("Average Load:", average_loads)
    plt.plot(list(average_loads.keys()), list(average_loads.values()), label=f'{n} servers')

plt.xlabel('Server ID')
plt.ylabel('Average Number of Requests Handled')
plt.title('Average Load Distribution Across Servers')
plt.legend()
plt.show()
