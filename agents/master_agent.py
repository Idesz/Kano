import json
import ollama
import logging
import asyncio
from core.model_router import ModelRouter
from core.skill_registry import SkillRegistry
from core.state_manager import StateManager
from core.memory import MemoryManager
from core.context_manager import ContextManager
from core.audit_logger import AuditLogger
from core.hallucination_detector import HallucinationDetector
from core.config import Config
from agents.base_agent import BaseAgent
from agents.coder_agent import CoderAgent
from agents.ingestor_agent import IngestorAgent
from agents.scaffold_agent import ScaffoldAgent
from agents.security_agent import SecurityAgent
from agents.browser_agent import BrowserAgent
from agents.roadmap_agent import RoadmapAgent

class MasterAgent(BaseAgent):
    def __init__(self):
        router = ModelRouter(default_model=Config.DEFAULT_MODEL)
        super().__init__("MasterAgent", router)
        self.registry = SkillRegistry()
        self.state = StateManager()
        self.memory = MemoryManager()
        self.context = ContextManager(self.memory)
        self.audit = AuditLogger()
        self.detector = HallucinationDetector(self.router)

        self.coder = CoderAgent(self.router)
        self.ingestor = IngestorAgent(self.router)
        self.scaffolder = ScaffoldAgent(self.router)
        self.security = SecurityAgent(self.router)
        self.browser = BrowserAgent(self.router)
        self.roadmap = RoadmapAgent(self.router)

    async def run_async(self, task: str, approved: bool = False):
        from core.guardrail import Guardrail
        allowed, msg = Guardrail.filter_input(task)
        if not allowed: return msg

        decision = await self.classify_intent_async(task)
        if decision.get("needs_approval") and not approved: return "APPROVAL_REQUIRED", decision.get("reason")

        target = decision.get("target")
        if target == "Roadmap": return self.roadmap.run(task)
        if target == "Browser": return self.browser.run(task)
        if target == "Security": return self.security.run(task)
        if target == "Scaffold": return self.scaffolder.run(task)
        if target == "Coder": return await self.coder.run_async(task)
        if target == "Ingestor": return self.ingestor.run(task)

        if target in self.registry.skills:
            return self.registry.execute_skill_isolated(target, **decision.get("parameters", {}))
        return f"Task {target} complete."

    async def classify_intent_async(self, user_input: str) -> dict:
        cache = self.state.get_decision_cache()
        if user_input in cache: return cache[user_input]

        relevant_context = self.context.retrieve_relevant_context(user_input)
        skills_list = self.registry.list_skills()
        prompt = f"Analyze request. Context: {relevant_context}\nSkills: {json.dumps(skills_list)}\nRequest: {user_input}"

        response = await self.router.generate_queued("reasoning", prompt, format="json")
        try:
            decision = json.loads(response['response'])
            self.state.update_decision_cache(user_input, decision)
            self.audit.log_decision(user_input, decision)
            return decision
        except Exception:
            return {"target": "Coder", "reason": "Fallback"}

    def run(self, task: str, approved: bool = False):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            # If the loop is already running (e.g., inside Textual), run it as a future
            return asyncio.run_coroutine_threadsafe(self.run_async(task, approved), loop).result()
        else:
            return loop.run_until_complete(self.run_async(task, approved))
