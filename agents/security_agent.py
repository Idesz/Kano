import ollama
from core.model_router import ModelRouter
from agents.base_agent import BaseAgent
from skills.code_auditor.code_auditor import CodeAuditor

class SecurityAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter):
        super().__init__("SecurityAgent", model_router)
        self.auditor = CodeAuditor()

    def provide_pentest_guidance(self, objective: str):
        """Reasoning logic similar to PentestGPT for strategic planning."""
        model = self.router.get_model_for_task("reasoning")
        prompt = f"""
        Act as a professional Penetration Tester.
        Analyze the following objective and provide a structured attack plan, including reconnaissance, vulnerability assessment, and potential exploitation steps.

        Objective: {objective}

        Provide the response in a structured 'Hacker' format.
        """
        response = ollama.generate(model=model, prompt=prompt)
        return response['response']

    def audit_code(self, code: str):
        """Static analysis combined with LLM security review."""
        static_results = self.auditor.execute(code)

        model = self.router.get_model_for_task("reasoning")
        prompt = f"Perform a deep security audit on the following Python code. Identify vulnerabilities and suggest fixes.\nCode:\n{code}"
        llm_response = ollama.generate(model=model, prompt=prompt)

        return {
            "static_analysis": static_results,
            "llm_review": llm_response['response']
        }

    def run(self, task: str):
        if "audit" in task.lower() or "security" in task.lower():
            # Logic would normally involve getting the code to audit
            return "Please provide the code block for security auditing."
        return self.provide_pentest_guidance(task)
