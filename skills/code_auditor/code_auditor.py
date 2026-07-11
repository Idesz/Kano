import re

class CodeAuditor:
    def execute(self, code: str):
        vulnerabilities = []

        # 1. Hardcoded Secrets
        if re.search(r'(api[_-]key|password|secret|token)\s*=\s*[\'"][^\'"]+[\'"]', code, re.I):
            vulnerabilities.append({"type": "Hardcoded Secret", "severity": "High", "desc": "Possible hardcoded API key or password detected."})

        # 2. SQL Injection patterns
        if re.search(r'\.execute\(f?["\'].*\{.*\}["\']\)', code):
            vulnerabilities.append({"type": "SQL Injection", "severity": "Critical", "desc": "Possible f-string or format-based SQL query detected."})

        # 3. Insecure usage of eval/exec
        if re.search(r'(eval|exec)\(.*\)', code):
            vulnerabilities.append({"type": "Dynamic Execution", "severity": "Medium", "desc": "Use of eval() or exec() can lead to arbitrary code execution."})

        if not vulnerabilities:
            return "No common vulnerabilities detected by static analysis."

        return vulnerabilities
