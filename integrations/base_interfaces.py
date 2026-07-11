from abc import ABC, abstractmethod

class GitHubIntegration(ABC):
    @abstractmethod
    def push_code(self, repo_url: str, files: list):
        pass

    @abstractmethod
    def create_pr(self, repo_url: str, title: str, body: str):
        pass

class SupabaseIntegration(ABC):
    @abstractmethod
    def query_db(self, query: str):
        pass

    @abstractmethod
    def insert_data(self, table: str, data: dict):
        pass
