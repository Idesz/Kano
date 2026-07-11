import subprocess
import os
import ollama
from core.model_router import ModelRouter
from agents.base_agent import BaseAgent

class ControlAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter = None):
        router = model_router or ModelRouter()
        super().__init__("ControlAgent", router)

    def check_syntax(self, code: str):
        temp_file = "temp_check.py"
        with open(temp_file, "w") as f:
            f.write(code)
        result = subprocess.run(["python", "-m", "py_compile", temp_file], capture_output=True, text=True)
        if os.path.exists(temp_file): os.remove(temp_file)
        if result.returncode != 0:
            return False, result.stderr
        return True, "No syntax errors"

    def generate_tests(self, code: str):
        model = self.router.get_model_for_task("coding")
        prompt = f"Write comprehensive pytest test cases for the following Python code. Return ONLY the test code.\nCode:\n{code}"
        response = ollama.generate(model=model, prompt=prompt)
        test_code = response['response'].strip()
        if "```" in test_code:
            test_code = test_code.split("```")[1].split("```")[0].replace("python", "").strip()
        return test_code

    def run_tests(self, code: str, tests: str):
        with open("tested_module.py", "w") as f:
            f.write(code)
        with open("test_module.py", "w") as f:
            f.write("from tested_module import *\n" + tests)

        result = subprocess.run(["pytest", "test_module.py"], capture_output=True, text=True)

        if os.path.exists("tested_module.py"): os.remove("tested_module.py")
        if os.path.exists("test_module.py"): os.remove("test_module.py")

        return result.returncode == 0, result.stdout + result.stderr

    def full_validation(self, code: str):
        valid, msg = self.check_syntax(code)
        if not valid:
            return False, f"Syntax Error: {msg}"
        tests = self.generate_tests(code)
        success, output = self.run_tests(code, tests)
        if not success:
            return False, f"Logic/Test Failure:\n{output}"
        return True, "Code passed syntax and functional tests."

    def run(self, task: str):
        return self.full_validation(task)
