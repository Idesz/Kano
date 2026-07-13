import json
import ollama
from agents.base_agent import BaseAgent
from core.state_manager import StateManager

class RoadmapAgent(BaseAgent):
    def __init__(self, model_router):
        super().__init__("RoadmapAgent", model_router)
        self.state = StateManager()

    def generate_roadmap(self, project_goal: str):
        model = self.router.get_model_for_task("reasoning")
        prompt = f"Senior Project Manager. Technical roadmap for: {project_goal}. Breakdown into Milestones and Tasks. JSON only."
        response = ollama.generate(model=model, prompt=prompt, format="json")
        roadmap = json.loads(response['response'])

        # Persistence
        project_name = roadmap.get("project_name", "unnamed_project")
        self.state.save_roadmap(project_name, roadmap)

        return roadmap

    def run(self, task: str):
        return self.generate_roadmap(task)
