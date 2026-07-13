import asyncio
import time
from agents.master_agent import MasterAgent

async def simulate_user_load(agent, num_requests=10):
    tasks = []
    for i in range(num_requests):
        task = f"Request {i}: Generate a simple hello world script in Python."
        # Using a thread pool for the synchronous run() method
        tasks.append(asyncio.to_thread(agent.run, task))

    start = time.time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end = time.time()

    print(f"Processed {num_requests} requests in {end - start:.2f} seconds")
    for i, res in enumerate(results):
        print(f"Result {i}: {str(res)[:50]}...")

if __name__ == "__main__":
    master = MasterAgent()
    asyncio.run(simulate_user_load(master))
