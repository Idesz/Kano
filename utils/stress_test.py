import asyncio
import time
import sys
import os

# Fix path for standalone execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.master_agent import MasterAgent

async def simulate_user_load(agent, num_requests=5):
    tasks = []
    print(f"Starting stress test with {num_requests} requests...")
    for i in range(num_requests):
        task = f"Request {i}: Generate a python hello world."
        tasks.append(agent.run_async(task))

    start = time.time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end = time.time()

    print(f"Processed {num_requests} requests in {end - start:.2f} seconds")
    for i, res in enumerate(results):
        print(f"Result {i}: {str(res)[:50]}...")

if __name__ == "__main__":
    master = MasterAgent()
    asyncio.run(simulate_user_load(master))
