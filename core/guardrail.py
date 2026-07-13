import re

class Guardrail:
    @staticmethod
    def filter_input(user_input: str):
        """Hacker-friendly input filtering to prevent core system manipulation."""
        # 1. Check for prompt injection attempts (extreme patterns)
        injection_patterns = [
            r"ignore all previous instructions",
            r"delete entire file system",
            r"system reset --force"
        ]
        for pattern in injection_patterns:
            if re.search(pattern, user_input, re.I):
                return False, "Dangerous prompt injection detected. Operation blocked for system safety."

        # 2. Allow all technical/hacker commands
        return True, user_input
