import ollama
from core.model_router import ModelRouter
from agents.control_agent import ControlAgent
from agents.base_agent import BaseAgent

class PerformanceAnalyzer(BaseAgent):
    def __init__(self, model_router: ModelRouter = None):
        router = model_router or ModelRouter()
        super().__init__("PerformanceAnalyzer", router)
        self.controller = ControlAgent(router)

    def execute(self, code: str):
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
        # Fixed: using self.controller.run() or a valid method
        success, output = self.controller.run(perf_script)

        if not success:
            return {"status": "Error", "message": output}

        try:
            time_val = float(output.split("PERF_TIME:")[1].split()[0].strip())
            return {"status": "Success", "execution_time_sec": time_val}
        except:
            return {"status": "Error", "message": "Failed to parse performance data"}
