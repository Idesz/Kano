import os
import json
import ollama
from core.model_router import ModelRouter
from agents.base_agent import BaseAgent

class ScaffoldAgent(BaseAgent):
    def __init__(self, model_router: ModelRouter = None):
        router = model_router or ModelRouter()
        super().__init__("ScaffoldAgent", router)
        self.blueprints_dir = "blueprints"

    def list_blueprints(self):
        return os.listdir(self.blueprints_dir) if os.path.exists(self.blueprints_dir) else []

    def create_project(self, blueprint_name: str, project_name: str):
        blueprint_path = os.path.join(self.blueprints_dir, blueprint_name)
        if not os.path.exists(blueprint_path):
            return f"Blueprint {blueprint_name} not found."

        with open(os.path.join(blueprint_path, "structure.json"), "r") as f:
            structure = json.load(f)

        os.makedirs(project_name, exist_ok=True)

        results = []
        for filename in structure["files"]:
            model = self.router.get_model_for_task("coding")
            prompt = f"Generate the content for the file '{filename}' in a {blueprint_name} project. Project goal: {project_name}. Code only."
            response = ollama.generate(model=model, prompt=prompt)
            content = response['response'].strip()
            if "```" in content: content = content.split("```")[1].split("```")[0].replace("python", "").strip()

            with open(os.path.join(project_name, filename), "w") as f:
                f.write(content)
            results.append(filename)

        return f"Project {project_name} scaffolded with files: {', '.join(results)}"

    def run(self, task: str):
        """Parses project name and blueprint from task."""
        # Simple extraction logic for demo
        project_name = "new_project"
        blueprint = "fastapi_supabase"

        if "named" in task.lower():
            project_name = task.split("named")[-1].strip().split()[0]

        return self.create_project(blueprint, project_name)
