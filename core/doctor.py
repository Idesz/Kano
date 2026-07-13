import subprocess
import requests
import os

class KanoDoctor:
    def __init__(self):
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def check_system(self):
        return {
            "Ollama API": self._check_ollama(),
            "Docker Engine": self._check_command(["docker", "info"]),
            "Network (Nmap)": self._check_command(["nmap", "--version"]),
            "Sandbox Image": self._check_docker_image("kano-sandbox:latest")
        }

    def _check_ollama(self):
        try:
            resp = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            return "READY" if resp.status_code == 200 else "ERROR (HTTP)"
        except:
            return "UNREACHABLE"

    def _check_docker_image(self, image_name):
        try:
            subprocess.run(["docker", "image", "inspect", image_name], capture_output=True, check=True)
            return "READY"
        except:
            return "MISSING (Will bootstrap on first use)"

    def _check_command(self, cmd):
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return "READY"
        except:
            return "MISSING"
