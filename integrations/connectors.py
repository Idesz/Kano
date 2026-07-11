import os
import subprocess

class GitHubConnector:
    def __init__(self, token: str = None):
        self.token = token or os.getenv("GITHUB_TOKEN")

    def clone(self, repo_url: str, dest: str):
        result = subprocess.run(["git", "clone", repo_url, dest], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr

    def commit_and_push(self, repo_path: str, message: str, branch: str = "main"):
        try:
            subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
            subprocess.run(["git", "-C", repo_path, "commit", "-m", message], check=True)
            subprocess.run(["git", "-C", repo_path, "push", "origin", branch], check=True)
            return "Successfully pushed changes"
        except Exception as e:
            return f"Git error: {e}"

class SupabaseConnector:
    def __init__(self, url: str = None, key: str = None):
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")

    def query(self, table: str, select: str = "*"):
        # Placeholder for actual supabase-py implementation
        return f"Querying {table} on Supabase... (Integration skeleton ready)"

    def insert(self, table: str, data: dict):
        return f"Inserting into {table} on Supabase... (Integration skeleton ready)"
