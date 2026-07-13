import json
import ollama
from agents.base_agent import BaseAgent

class RoadmapAgent(BaseAgent):
    def __init__(self, model_router):
        super().__init__("RoadmapAgent", model_router)
        self.milestones = []
        self.tasks = []

    def generate_roadmap(self, project_goal: str):
        """Generates a structured roadmap for a new project."""
        model = self.router.get_model_for_task("reasoning")
        prompt = f"""
        You are a Senior Project Manager. Create a detailed technical roadmap for the following goal: {project_goal}
        Break it down into Milestones and individual Tasks.

        Return valid JSON:
        {{
            "project_name": "...",
            "milestones": [
                {{
                    "title": "...",
                    "tasks": ["task1", "task2"]
                }}
            ]
        }}
        """
        response = ollama.generate(model=model, prompt=prompt, format="json")
        roadmap = json.loads(response['response'])
        self.milestones = roadmap.get("milestones", [])
        return roadmap

    def get_next_task(self):
        """Returns the next pending task from the current roadmap."""
        for milestone in self.milestones:
            for task in milestone.get("tasks", []):
                # Simplified check: return the first one for now
                return task
        return "All tasks completed."

    def run(self, task: str):
        return self.generate_roadmap(task)
