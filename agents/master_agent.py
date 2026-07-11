import json
import ollama
from core.model_router import ModelRouter
from core.skill_registry import SkillRegistry
from agents.base_agent import BaseAgent

class MasterAgent(BaseAgent):
    def __init__(self):
        self.router = ModelRouter()
        super().__init__("MasterAgent", self.router)
        self.registry = SkillRegistry()
        self.decision_cache = {} # Simple cache for intent classification

    def classify_intent(self, user_input: str) -> dict:
        """Uses LLM to decide which skill or agent is needed."""
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
        except Exception as e:
            # Fallback logic if LLM fails or isn't connected
            return {"target": "Coder", "reason": "Fallback due to error", "parameters": {}}

    def run(self, task: str):
        decision = self.classify_intent(task)
        target = decision.get("target")
        return f"Decision: {target} because {decision.get('reason')}"

if __name__ == "__main__":
    master = MasterAgent()
    print(master.classify_intent("Create a simple calculator in Python"))
