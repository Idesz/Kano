import subprocess

class NetworkScanner:
    def execute(self, target: str, scan_type: str = "quick"):
        if scan_type == "quick":
            # Simple port check (this assumes nmap is installed on the host)
            try:
                result = subprocess.run(["nmap", "-F", target], capture_output=True, text=True)
                return result.stdout if result.returncode == 0 else result.stderr
            except FileNotFoundError:
                return "nmap not found. Please install nmap for network scanning capabilities."
        return "Unsupported scan type"
