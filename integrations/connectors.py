import os
import subprocess
import requests

class GitHubConnector:
    def __init__(self, token: str = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {"Authorization": f"token {self.token}"} if self.token else {}

    def create_repo(self, name: str, private: bool = True):
        url = "https://api.github.com/user/repos"
        data = {"name": name, "private": private}
        resp = requests.post(url, json=data, headers=self.headers)
        return resp.json()

    def commit_and_push(self, repo_path: str, message: str, branch: str = "main"):
        try:
            subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
            subprocess.run(["git", "-C", repo_path, "commit", "-m", message], check=True)
            subprocess.run(["git", "-C", repo_path, "push", "origin", branch], check=True)
            return "Pushed to GitHub."
        except Exception as e:
            return f"Git error: {e}"

class SupabaseConnector:
    def __init__(self, url: str = None, key: str = None):
        self.url = (url or os.getenv("SUPABASE_URL", "")).rstrip('/')
        self.key = key or os.getenv("SUPABASE_KEY", "")
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }

    def query(self, table: str, select: str = "*"):
        url = f"{self.url}/rest/v1/{table}?select={select}"
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def insert(self, table: str, data: dict):
        url = f"{self.url}/rest/v1/{table}"
        resp = requests.post(url, json=data, headers=self.headers)
        return resp.status_code
