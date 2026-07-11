import json
import ollama
import logging
import os
import re
from core.model_router import ModelRouter
from core.skill_registry import SkillRegistry
from agents.base_agent import BaseAgent
from agents.coder_agent import CoderAgent
from agents.ingestor_agent import IngestorAgent
from agents.scaffold_agent import ScaffoldAgent
from agents.security_agent import SecurityAgent

class MasterAgent(BaseAgent):
    def __init__(self):
        router = ModelRouter()
        super().__init__("MasterAgent", router)
        self.registry = SkillRegistry()
        self.coder = CoderAgent(self.router)
        self.ingestor = IngestorAgent(self.router)
        self.scaffolder = ScaffoldAgent(self.router)
        self.security = SecurityAgent(self.router)
        self.decision_cache = {}
        logging.basicConfig(level=logging.INFO)

    def classify_intent(self, user_input: str) -> dict:
        if user_input in self.decision_cache:
            return self.decision_cache[user_input]

        skills_list = self.registry.list_skills()
        blueprints = self.scaffolder.list_blueprints()

        prompt = f"""
        Analyze the following user request and determine the target agent or skill.
        Available Skills: {json.dumps(skills_list)}
        Worker Agents: Coder, Scaffold, Ingestor, Repo, Database, Security (pentesting/auditing).

        - OBJECTIVE: Logic, algorithms, data.
        - SUBJECTIVE: UI/UX, design.
        - SECURITY: Pentesting, scanning, auditing.

        Response must be valid JSON:
        {{
            "target": "skill_name or agent_name or SkillCreator or Scaffold",
            "reason": "short explanation",
            "needs_approval": true/false,
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
            return {"target": "Coder", "reason": "Fallback", "needs_approval": False, "parameters": {}}

    def run(self, task: str, approved: bool = False):
        decision = self.classify_intent(task)
        if decision.get("needs_approval") and not approved:
            return "APPROVAL_REQUIRED", decision.get("reason")

        target = decision.get("target")

        if "youtube.com" in task or "youtu.be" in task:
            target = "media_fetcher"
            decision["parameters"]["url"] = re.findall(r'(https?://\S+)', task)[0]
            decision["parameters"]["action"] = "get_info"

        if target == "Security":
            return self.security.run(task)
        elif target == "SkillCreator":
            return self.create_new_skill(decision.get("new_skill_name", "new_skill"), task)
        elif target == "Scaffold":
            return self.scaffolder.create_project(decision.get("blueprint", "fastapi_supabase"), "generated_project")
        elif target == "Coder":
            return self.coder.run(task)
        elif target == "Ingestor":
            return self.ingestor.run(task)
        elif target in self.registry.skills:
            skill_info = self.registry.get_skill(target)
            skill_instance = skill_info["class"]()
            return skill_instance.execute(**decision.get("parameters", {}))

        return f"Decision: {target} (Executing...)"

    def create_new_skill(self, skill_name: str, objective: str):
        logging.info(f"Creating new skill: {skill_name}")
        metadata_prompt = f"Create a metadata.json for a Kano skill named '{skill_name}' that does: {objective}. Return valid JSON."
        model = self.router.get_model_for_task("reasoning")
        meta_resp = ollama.generate(model=model, prompt=metadata_prompt, format="json")
        metadata = json.loads(meta_resp['response'])

        code_prompt = f"Write a Python class for a Kano skill named '{skill_name}'. It should have an 'execute' method. Objective: {objective}. Code only."
        code, status = self.coder.run(code_prompt)

        skill_dir = os.path.join("skills", skill_name)
        os.makedirs(skill_dir, exist_ok=True)
        with open(os.path.join(skill_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=4)
        with open(os.path.join(skill_dir, f"{skill_name}.py"), "w") as f:
            f.write(code)

        self.registry.load_skills()
        return f"Successfully created and registered new skill: {skill_name}"
