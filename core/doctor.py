import subprocess
import logging

class KanoDoctor:
    def check_system(self):
        results = {
            "Ollama": self._check_command(["ollama", "--version"]),
            "Docker": self._check_command(["docker", "--version"]),
            "Nmap": self._check_command(["nmap", "--version"]),
            "Playwright": self._check_command(["playwright", "--version"])
        }
        return results

    def _check_command(self, cmd):
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return "READY"
        except Exception:
            return "MISSING"

if __name__ == "__main__":
    doctor = KanoDoctor()
    print(doctor.check_system())
