import json
import ollama
import logging
from core.model_router import ModelRouter
from core.skill_registry import SkillRegistry
from agents.base_agent import BaseAgent
from agents.coder_agent import CoderAgent
from agents.ingestor_agent import IngestorAgent

class MasterAgent(BaseAgent):
    def __init__(self):
        self.router = ModelRouter()
        super().__init__("MasterAgent", self.router)
        self.registry = SkillRegistry()
        self.coder = CoderAgent(self.router)
        self.ingestor = IngestorAgent(self.router)
        self.decision_cache = {}
        logging.basicConfig(level=logging.INFO)

    def classify_intent(self, user_input: str) -> dict:
        if user_input in self.decision_cache:
            return self.decision_cache[user_input]

        skills_list = self.registry.list_skills()
        prompt = f"""
        Analyze the following user request and determine which skill or worker agent should handle it.
        Available Skills: {json.dumps(skills_list)}
        Worker Agents: Coder, Ingestor, Repo, Database.

        Response must be valid JSON:
        {{
            "target": "skill_name or agent_name",
            "reason": "short explanation",
            "parameters": {{}}
        }}

        Request: "{user_input}"
        """

        model = self.router.get_model_for_task("reasoning")
        try:
            response = ollama.generate(model=model, prompt=prompt, format="json")
            decision = json.loads(response['response'])
            self.decision_cache[user_input] = decision
            return decision
        except Exception:
            return {"target": "Coder", "reason": "Fallback", "parameters": {}}

    def run(self, task: str):
        decision = self.classify_intent(task)
        target = decision.get("target")

        if target == "Coder":
            return self.coder.run(task)
        elif target == "Ingestor":
            url = decision.get("parameters", {}).get("url")
            if not url and "http" in task:
                import re
                urls = re.findall(r'(https?://\S+)', task)
                url = urls[0] if urls else ""
            return self.ingestor.run(url or task)
        elif target in self.registry.skills:
            skill_info = self.registry.get_skill(target)
            skill_instance = skill_info["class"]()
            return skill_instance.execute(**decision.get("parameters", {}))

        return f"Decision: {target} (Under development)"
