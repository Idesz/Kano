from agents.control_agent import ControlAgent

class PerformanceAnalyzer:
    def __init__(self):
        self.controller = ControlAgent()

    def execute(self, code: str):
        """Measures the performance of a given code snippet using the secure Docker sandbox."""
        perf_script = f"""
import time
import os
import sys

start_time = time.time()
try:
    {code}
    end_time = time.time()
    print(f"PERF_TIME:{{end_time - start_time}}")
except Exception as e:
    print(f"PERF_ERROR:{{e}}")
    sys.exit(1)
"""
        success, output = self.controller.run_tests(perf_script, "")

        if not success:
            return {"status": "Error", "message": output}

        # Parse time from output
        try:
            time_val = float(output.split("PERF_TIME:")[1].strip())
            return {"status": "Success", "execution_time_sec": time_val}
        except:
            return {"status": "Error", "message": "Failed to parse performance data"}
