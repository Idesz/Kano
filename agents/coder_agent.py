import ollama
from core.model_router import ModelRouter
from agents.control_agent import ControlAgent

class CoderAgent:
    def __init__(self, model_router: ModelRouter):
        self.router = model_router
        self.controller = ControlAgent()

    def generate_code(self, prompt: str):
        model = self.router.get_model_for_task("coding")
        full_prompt = f"Write Python code for the following task. Return ONLY the code, no explanation.\nTask: {prompt}"

        response = ollama.generate(model=model, prompt=full_prompt)
        code = response['response'].strip()

        # Clean up common LLM markdown if present
        if code.startswith("```python"):
            code = code.split("```python")[1].split("```")[0].strip()
        elif code.startswith("```"):
            code = code.split("```")[1].split("```")[0].strip()

        return code

    def autonomous_fix_loop(self, prompt: str, max_iterations: int = 3):
        """Iteratively generates and fixes code until it passes syntax check."""
        code = self.generate_code(prompt)

        for i in range(max_iterations):
            is_valid, error = self.controller.check_syntax(code)
            if is_valid:
                return code, f"Success after {i} iterations"

            # Request fix from LLM
            model = self.router.get_model_for_task("coding")
            fix_prompt = f"The following Python code has a syntax error. Please fix it.\nCode:\n{code}\nError:\n{error}\nReturn ONLY the fixed code."
            response = ollama.generate(model=model, prompt=fix_prompt)
            code = response['response'].strip()

            if code.startswith("```"): # Basic cleaning
                code = code.split("```")[1].split("```")[0].replace("python", "").strip()

        return code, "Failed to fix after max iterations"
