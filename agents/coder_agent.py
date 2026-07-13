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
        system_prompt = self.ponytail.get_system_prompt()
        full_prompt = f"{system_prompt}\n\nTask: {prompt}\n\nReturn ONLY code."
        response = ollama.generate(model=model, prompt=full_prompt)
        code = response['response'].strip()
        if "```" in code: code = code.split("```")[1].split("```")[0].replace("python", "").strip()
        return code

    def run(self, task: str):
        code = self.generate_code(task)

        for i in range(5):
            valid, report = self.controller.full_validation(code)

            # Continuous Vision Audit for UI code
            if "html" in task.lower() or "css" in task.lower():
                # visual_check = self.vision.execute("sandbox/screenshot.png", "Identify UI issues.")
                # report += f"\nVision Audit: {visual_check}"
                pass

            if valid: return code, f"Transcendent Success (Iteration {i+1})"

            model = self.router.get_model_for_task("coding")
            fix_prompt = f"Fix this code.\nCode:\n{code}\nError Report:\n{report}\nReturn ONLY fixed code."
            resp = ollama.generate(model=model, prompt=fix_prompt)
            code = resp['response'].strip()
            if "```" in code: code = code.split("```")[1].split("```")[0].replace("python", "").strip()

        return code, "Max iterations reached."
