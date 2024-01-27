import asyncio
import aiohttp
import matplotlib.pyplot as plt

async def send_request(session, url):
    async with session.get(url) as response:
        return await response.text()

async def test_load_distribution(server_count):
    url = "http://localhost:8000/home"  # Adjust if your load balancer is on a different port
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

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(server_counts.keys(), server_counts.values())
        plt.xlabel('Server ID')
        plt.ylabel('Number of Requests Handled')
        plt.title(f'Load Distribution Among {server_count} Servers')
        plt.show()

for n in range(2, 7):  # For N from 2 to 6
    print(f"Testing with {n} servers...")
    # Ensure that n server instances are running before proceeding
    asyncio.run(test_load_distribution(n))
