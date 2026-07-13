import asyncio
from agents.base_agent import BaseAgent
from skills.browser_operator.browser_operator import BrowserOperator

class BrowserAgent(BaseAgent):
    def __init__(self, model_router):
        super().__init__("BrowserAgent", model_router)
        self.operator = BrowserOperator()

    def handle_interactive_task(self, task: str):
        """
        Uses LLM to decompose a natural language web task into Playwright actions.
        Example: 'Go to github and search for kano'
        """
        model = self.router.get_model_for_task("reasoning")
        prompt = f"""
        Decompose the following web task into a sequence of Playwright actions (navigate, click, type, screenshot).
        Task: {task}

        Return a JSON list of actions:
        [
            {{"action": "navigate", "url": "https://..."}},
            {{"action": "type", "selector": "#search", "text": "..."}},
            {{"action": "click", "selector": "button[type=submit]"}}
        ]
        """
        # Logic to call LLM and then loop through self.operator.run_sync for each action
        return "Browser interaction sequence initialized. (Skeleton ready)"

    def run(self, task: str):
        return self.handle_interactive_task(task)
