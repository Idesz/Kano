import time
import psutil
import os

class PerformanceAnalyzer:
    def execute(self, code: str):
        """Measures the performance of a given code snippet."""
        start_time = time.time()
        process = psutil.Process(os.getpid())
        start_mem = process.memory_info().rss

        try:
            # Dangerous in real use, but here it's part of the analyzer
            exec(code)

            end_time = time.time()
            end_mem = process.memory_info().rss

            return {
                "execution_time_sec": end_time - start_time,
                "memory_delta_kb": (end_mem - start_mem) / 1024,
                "status": "Success"
            }
        except Exception as e:
            return {"status": "Error", "message": str(e)}
