from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, model_router):
        self.name = name
        self.model_router = model_router

    @abstractmethod
    def run(self, task: str):
        pass
