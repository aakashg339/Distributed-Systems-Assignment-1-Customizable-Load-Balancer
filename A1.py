import asyncio
import aiohttp
import matplotlib.pyplot as plt

async def send_request(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    url = "http://localhost:8000/home"  # Load balancer URL
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        for _ in range(10000):
            task = asyncio.ensure_future(send_request(session, url))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        # Count requests handled by each server
        server_counts = {}
        for response in responses:
            server_id = response.split()[-1]  # Assuming the response format is "Hello from Server: X"
            server_counts[server_id] = server_counts.get(server_id, 0) + 1

        # Plotting
        plt.bar(server_counts.keys(), server_counts.values())
        plt.xlabel('Server ID')
        plt.ylabel('Number of Requests Handled')
        plt.title('Load Distribution Among Servers')
        plt.show()

# Run the asyncio event loop
asyncio.run(main())
