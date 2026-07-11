import ollama
from core.model_router import ModelRouter
from agents.control_agent import ControlAgent
from agents.base_agent import BaseAgent

class CoderAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter):
        super().__init__("CoderAgent", model_router)
        self.controller = ControlAgent(model_router)

    def generate_code(self, prompt: str):
        model = self.router.get_model_for_task("coding")
        full_prompt = f"Write Python code for the following task. Return ONLY the code, no explanation.\nTask: {prompt}"
        response = ollama.generate(model=model, prompt=full_prompt)
        code = response['response'].strip()
        if "```" in code:
            code = code.split("```")[1].split("```")[0].replace("python", "").strip()
        return code

    def autonomous_fix_loop(self, prompt: str, max_iterations: int = 5):
        code = self.generate_code(prompt)

        for i in range(max_iterations):
            is_valid, report = self.controller.full_validation(code)
            if is_valid:
                return code, f"Success after {i+1} iterations"

            model = self.router.get_model_for_task("coding")
            fix_prompt = f"The following Python code has errors.\nCode:\n{code}\nValidation Report:\n{report}\n\nPlease fix the code and return ONLY the fixed code."
            response = ollama.generate(model=model, prompt=fix_prompt)
            code = response['response'].strip()
            if "```" in code:
                code = code.split("```")[1].split("```")[0].replace("python", "").strip()

        return code, f"Failed to pass validation after {max_iterations} iterations. Last report: {report}"

    def run(self, task: str):
        return self.autonomous_fix_loop(task)
