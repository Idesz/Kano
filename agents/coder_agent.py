import ollama
from core.model_router import ModelRouter
from agents.control_agent import ControlAgent
from agents.base_agent import BaseAgent
from skills.ponytail.ponytail import Ponytail
from skills.visual_analyzer.visual_analyzer import VisualAnalyzer

class CoderAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter):
        super().__init__("CoderAgent", model_router)
        self.controller = ControlAgent(model_router)
        self.ponytail = Ponytail()
        self.vision = VisualAnalyzer()

    def generate_code(self, prompt: str, lazy_mode: bool = True):
        model = self.router.get_model_for_task("coding")
        system_prompt = self.ponytail.get_system_prompt() if lazy_mode else "You are a professional Python developer."
        full_prompt = f"{system_prompt}\n\nTask: {prompt}\n\nReturn ONLY the code, no explanation."
        response = ollama.generate(model=model, prompt=full_prompt)
        code = response['response'].strip()
        if "```" in code: code = code.split("```")[1].split("```")[0].replace("python", "").strip()
        return code

    def autonomous_fix_loop(self, prompt: str, max_iterations: int = 5):
        code = self.generate_code(prompt)

        for i in range(max_iterations):
            is_valid, report = self.controller.full_validation(code)

            # Visual Feedback logic: If it's UI code, we could screenshot and analyze here
            if "html" in prompt.lower() or "css" in prompt.lower():
                 # Placeholder for capturing screenshot from sandbox/browser
                 # visual_report = self.vision.execute("screenshot.png", "Does this UI look correct?")
                 pass

            if is_valid:
                return code, f"Success after {i+1} iterations (Ponytail Mode: Active)"

            model = self.router.get_model_for_task("coding")
            fix_prompt = f"The following code has errors. Fix it using the minimum code possible.\nCode:\n{code}\nReport:\n{report}\nReturn ONLY fixed code."
            response = ollama.generate(model=model, prompt=fix_prompt)
            code = response['response'].strip()
            if "```" in code: code = code.split("```")[1].split("```")[0].replace("python", "").strip()

        return code, f"Failed after {max_iterations} iterations. Last report: {report}"

    def run(self, task: str):
        return self.autonomous_fix_loop(task)
