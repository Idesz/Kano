import subprocess
import os
import ollama
from core.model_router import ModelRouter
from agents.base_agent import BaseAgent

class ControlAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter = None):
        router = model_router or ModelRouter()
        super().__init__("ControlAgent", router)

    def _run_in_docker(self, code: str, command: list):
        """Runs the provided code in an isolated Docker container."""
        # Create a workspace
        os.makedirs("sandbox", exist_ok=True)
        with open("sandbox/script.py", "w") as f:
            f.write(code)

        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}/sandbox:/app",
            "-w", "/app",
            "python:3.11-slim"
        ] + command

        result = subprocess.run(docker_cmd, capture_output=True, text=True)
        return result

    def check_syntax(self, code: str):
        # We can still do syntax check locally for speed, or via Docker
        temp_file = "temp_check.py"
        with open(temp_file, "w") as f:
            f.write(code)
        result = subprocess.run(["python", "-m", "py_compile", temp_file], capture_output=True, text=True)
        if os.path.exists(temp_file): os.remove(temp_file)
        if result.returncode != 0:
            return False, result.stderr
        return True, "No syntax errors"

    def run_tests(self, code: str, tests: str):
        """Runs pytest inside a Docker container."""
        full_code = f"with open('tested_module.py', 'w') as f: f.write({repr(code)})\n"
        full_code += f"with open('test_module.py', 'w') as f: f.write('from tested_module import *\\n' + {repr(tests)})\n"
        full_code += "import subprocess; subprocess.run(['pip', 'install', 'pytest'], capture_output=True); "
        full_code += "res = subprocess.run(['pytest', 'test_module.py'], capture_output=True, text=True); "
        full_code += "print(res.stdout + res.stderr); exit(res.returncode)"

        result = self._run_in_docker(full_code, ["python", "-c", full_code])
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
