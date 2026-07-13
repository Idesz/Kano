import subprocess
import os
import ollama
import logging
from core.model_router import ModelRouter
from agents.base_agent import BaseAgent

class ControlAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter = None):
        router = model_router or ModelRouter()
        super().__init__("ControlAgent", router)
        self.sandbox_image = "kano-sandbox:latest"
        self._bootstrap_sandbox()

    def _bootstrap_sandbox(self):
        """Ensures the kano-sandbox image exists, builds it if missing."""
        try:
            check_cmd = ["docker", "image", "inspect", self.sandbox_image]
            subprocess.run(check_cmd, capture_output=True, check=True)
            logging.info("Kano Sandbox image ready.")
        except subprocess.CalledProcessError:
            logging.info("Building Kano Sandbox image (first-time setup)...")
            build_cmd = ["docker", "build", "-t", self.sandbox_image, "-f", "sandbox.Dockerfile", "."]
            try:
                subprocess.run(build_cmd, check=True)
                logging.info("Kano Sandbox image built successfully.")
            except Exception as e:
                logging.error(f"Failed to build sandbox image: {e}")

    def _run_in_docker(self, script_content: str, timeout: int = 30):
        os.makedirs("sandbox", exist_ok=True)
        with open("sandbox/runner.py", "w") as f:
            f.write(script_content)

        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "-v", f"{os.getcwd()}/sandbox:/app",
            "-w", "/app",
            self.sandbox_image,
            "python", "runner.py"
        ]

        try:
            result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=timeout)
            return result
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(args=docker_cmd, returncode=124, stdout="", stderr="Execution Timed Out")

    def full_validation(self, code: str):
        model = self.router.get_model_for_task("coding")
        test_prompt = f"Write comprehensive pytest test cases for the following code. Return ONLY test code.\nCode:\n{code}"
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
    print(f"Runner error: {{e}}")
    sys.exit(1)
"""
        result = self._run_in_docker(runner_script)
        return result.returncode == 0, result.stdout + result.stderr

    def run(self, task: str):
        return self.full_validation(task)
