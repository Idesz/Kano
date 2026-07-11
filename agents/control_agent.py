import subprocess
import os

class ControlAgent:
    def __init__(self):
        pass

    def check_syntax(self, code: str):
        """Checks for syntax errors using 'python -m py_compile'."""
        temp_file = "temp_check.py"
        with open(temp_file, "w") as f:
            f.write(code)

        result = subprocess.run(["python", "-m", "py_compile", temp_file], capture_output=True, text=True)
        os.remove(temp_file)

        if result.returncode != 0:
            return False, result.stderr
        return True, "No syntax errors"

    def run_tests(self, test_file: str):
        """Runs pytest on the specified file."""
        result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr

    def validate_logic(self, code: str, expected_output: str):
        """Basic logic validation by running the code and comparing output."""
        # This is simplified for the skeleton
        pass
