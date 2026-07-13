import ollama
from core.model_router import ModelRouter
from agents.control_agent import ControlAgent
from agents.base_agent import BaseAgent
from skills.ponytail.ponytail import Ponytail
from skills.visual_analyzer.visual_analyzer import VisualAnalyzer
import asyncio

class CoderAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter):
        super().__init__("CoderAgent", model_router)
        self.controller = ControlAgent(model_router)
        self.ponytail = Ponytail()
        self.vision = VisualAnalyzer(model_router)

    async def generate_code(self, prompt: str):
        system_prompt = self.ponytail.get_system_prompt()
        full_prompt = f"{system_prompt}\n\nTask: {prompt}\n\nReturn ONLY code."
        response = await self.router.generate_queued("coding", full_prompt)
        code = response['response'].strip()
        if "```" in code: code = code.split("```")[1].split("```")[0].replace("python", "").strip()
        return code

    async def run_async(self, task: str):
        """Asynchronous version of the self-healing loop."""
        code = await self.generate_code(task)
        for i in range(5):
            valid, report = self.controller.full_validation(code)
            if valid: return code, f"Success (Iteration {i+1})"

            fix_prompt = f"Fix this code.\nCode:\n{code}\nError Report:\n{report}\nReturn ONLY fixed code."
            resp = await self.router.generate_queued("coding", fix_prompt)
            code = resp['response'].strip()
            if "```" in code: code = code.split("```")[1].split("```")[0].replace("python", "").strip()
        return code, "Max iterations reached."

    def run(self, task: str):
        # Fallback for sync callers
        return asyncio.run(self.run_async(task))
