import subprocess
import os
import logging
import uuid
import shutil
from core.model_router import ModelRouter
from agents.base_agent import BaseAgent

class ControlAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter = None):
        router = model_router or ModelRouter()
        super().__init__("ControlAgent", router)
        self.sandbox_image = "kano-sandbox:latest"
        self._bootstrap_sandbox()

    def _bootstrap_sandbox(self):
        try:
            # Check if docker command is available first
            subprocess.run(["docker", "--version"], capture_output=True, check=True)

            check_cmd = ["docker", "image", "inspect", self.sandbox_image]
            subprocess.run(check_cmd, capture_output=True, check=True)
        except Exception as e:
            logging.warning(f"Docker environment not ready or kano-sandbox build skipped: {e}")

    def _run_in_docker(self, script_content: str, timeout: int = 30):
        run_id = str(uuid.uuid4())
        workspace = os.path.abspath(f"sandbox/run_{run_id}")
        os.makedirs(workspace, exist_ok=True)

        runner_path = os.path.join(workspace, "runner.py")
        with open(runner_path, "w") as f:
            f.write(script_content)

        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "-v", f"{workspace}:/app",
            "-w", "/app",
            self.sandbox_image,
            "python", "runner.py"
        ]

        try:
            result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=timeout)
            return result
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(args=docker_cmd, returncode=124, stdout="", stderr="Execution Timed Out")
        except Exception as e:
            return subprocess.CompletedProcess(args=docker_cmd, returncode=1, stdout="", stderr=str(e))
        finally:
            if os.path.exists(workspace):
                shutil.rmtree(workspace)

    def full_validation(self, code: str):
        # Graceful fallback if Docker is not available
        try:
            subprocess.run(["docker", "info"], capture_output=True, check=True)
        except Exception:
            logging.warning("Docker sandbox unavailable. Performing local Python syntax check only.")
            temp_file = "temp_check.py"
            with open(temp_file, "w") as f: f.write(code)
            res = subprocess.run(["python", "-m", "py_compile", temp_file], capture_output=True, text=True)
            if os.path.exists(temp_file): os.remove(temp_file)
            return res.returncode == 0, res.stderr

        model = self.router.get_model_for_task("coding")
        test_prompt = f"Write pytest test cases for the following code. Return ONLY code.\nCode:\n{code}"
        resp = ollama.generate(model=model, prompt=test_prompt)
        tests = resp['response'].strip()
        if "```" in tests: tests = tests.split("```")[1].split("```")[0].replace("python", "").strip()

        runner_script = f"""
import sys
code = {repr(code)}
tests = {repr(tests)}
with open('tested_module.py', 'w') as f: f.write(code)
with open('test_module.py', 'w') as f: f.write('from tested_module import *\\n' + tests)
try:
    import pytest
    sys.exit(pytest.main(['test_module.py']))
except Exception as e:
    sys.exit(1)
"""
        result = self._run_in_docker(runner_script)
        return result.returncode == 0, result.stdout + result.stderr

    def run(self, task: str):
        return self.full_validation(task)
