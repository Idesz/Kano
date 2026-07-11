from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, model_router):
        self.name = name
        self.router = model_router # Unified naming

    @abstractmethod
    def run(self, task: str):
        pass
