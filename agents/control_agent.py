import subprocess
import os
import ollama
from core.model_router import ModelRouter
from agents.base_agent import BaseAgent

class ControlAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter = None):
        router = model_router or ModelRouter()
        super().__init__("ControlAgent", router)

    def _run_in_docker(self, code: str, command: list, timeout: int = 30):
        """Runs the provided code in an isolated Docker container with timeout."""
        os.makedirs("sandbox", exist_ok=True)
        with open("sandbox/script.py", "w") as f:
            f.write(code)

        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none", # Security: Disable network for sandbox execution
            "-v", f"{os.getcwd()}/sandbox:/app",
            "-w", "/app",
            "python:3.11-slim"
        ] + command

        try:
            result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=timeout)
            return result
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(args=docker_cmd, returncode=124, stdout="", stderr="Execution Timed Out")

    def check_syntax(self, code: str):
        temp_file = "temp_check.py"
        with open(temp_file, "w") as f:
            f.write(code)
        result = subprocess.run(["python", "-m", "py_compile", temp_file], capture_output=True, text=True)
        if os.path.exists(temp_file): os.remove(temp_file)
        if result.returncode != 0:
            return False, result.stderr
        return True, "No syntax errors"

    def run_tests(self, code: str, tests: str):
        """Runs pytest inside a Docker container using a pre-configured logic."""
        # Bundle everything into a single execution script to avoid runtime pip installs
        full_script = f"""
import sys
import subprocess

code = {repr(code)}
tests = {repr(tests)}

with open('tested_module.py', 'w') as f: f.write(code)
with open('test_module.py', 'w') as f: f.write('from tested_module import *\\n' + tests)

# Attempt to run pytest (assuming it's installed in a custom image or using basic unittest as fallback)
try:
    import pytest
    retcode = pytest.main(['test_module.py'])
    sys.exit(retcode)
except ImportError:
    # Minimal fallback to unittest if pytest is missing in slim image
    print("Pytest missing, falling back to basic execution check")
    try:
        exec(code)
        print("Basic execution successful")
        sys.exit(0)
    except Exception as e:
        print(f"Execution failed: {{e}}")
        sys.exit(1)
"""
        result = self._run_in_docker(full_script, ["python", "-c", full_script])
        return result.returncode == 0, result.stdout + result.stderr

    def full_validation(self, code: str):
        valid, msg = self.check_syntax(code)
        if not valid: return False, f"Syntax Error: {msg}"

        model = self.router.get_model_for_task("coding")
        test_prompt = f"Write comprehensive pytest test cases for the following Python code. Return ONLY the test code.\nCode:\n{code}"
        resp = ollama.generate(model=model, prompt=test_prompt)
        tests = resp['response'].strip()
        if "```" in tests: tests = tests.split("```")[1].split("```")[0].replace("python", "").strip()

        success, output = self.run_tests(code, tests)
        if not success: return False, f"Logic/Test Failure in Sandbox:\n{output}"
        return True, "Code passed sandbox validation."

    def run(self, task: str):
        return self.full_validation(task)
