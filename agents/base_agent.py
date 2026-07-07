from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, model_router):
        self.name = name
        self.model_router = model_router

    @abstractmethod
    def run(self, task: str):
        pass

class MasterAgent(BaseAgent):
    def __init__(self, model_router):
        super().__init__("MasterAgent", model_router)
        self.workers = {}

    def run(self, task: str):
        # Logic to delegate tasks to workers
        pass

class CoderAgent(BaseAgent):
    def run(self, task: str):
        model = self.model_router.get_model_for_task("coding")
        # Logic for coding
        pass
