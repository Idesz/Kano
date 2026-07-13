import subprocess
import os
import ollama
from core.model_router import ModelRouter
from agents.base_agent import BaseAgent

class ControlAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter = None):
        router = model_router or ModelRouter()
        super().__init__("ControlAgent", router)
        self.sandbox_image = os.getenv("DOCKER_IMAGE", "python:3.11-slim")

    def _run_in_docker(self, code: str, command: list, timeout: int = 60):
        os.makedirs("sandbox", exist_ok=True)
        with open("sandbox/script.py", "w") as f:
            f.write(code)

        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "-v", f"{os.getcwd()}/sandbox:/app",
            "-w", "/app",
            self.sandbox_image
        ] + command

        try:
            result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=timeout)
            return result
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(args=docker_cmd, returncode=124, stdout="", stderr="Execution Timed Out")

    def full_validation(self, code: str):
        # 1. Syntax check
        temp_file = "temp_check.py"
        with open(temp_file, "w") as f: f.write(code)
        syntax_res = subprocess.run(["python", "-m", "py_compile", temp_file], capture_output=True, text=True)
        if os.path.exists(temp_file): os.remove(temp_file)
        if syntax_res.returncode != 0: return False, f"Syntax Error: {syntax_res.stderr}"

        # 2. Functional check in Docker
        model = self.router.get_model_for_task("coding")
        test_prompt = f"Write comprehensive pytest test cases for the following code. Return ONLY test code.\nCode:\n{code}"
        resp = ollama.generate(model=model, prompt=test_prompt)
        tests = resp['response'].strip()
        if "```" in tests: tests = tests.split("```")[1].split("```")[0].replace("python", "").strip()

        full_script = f"""
import sys
code = {repr(code)}
tests = {repr(tests)}
with open('tested_module.py', 'w') as f: f.write(code)
with open('test_module.py', 'w') as f: f.write('from tested_module import *\\n' + tests)
import subprocess
try:
    import pytest
    sys.exit(pytest.main(['test_module.py']))
except ImportError:
    try:
        exec(code)
        sys.exit(0)
    except: sys.exit(1)
"""
        result = self._run_in_docker(full_script, ["python", "-c", full_script])
        return result.returncode == 0, result.stdout + result.stderr

    def run(self, task: str):
        return self.full_validation(task)
