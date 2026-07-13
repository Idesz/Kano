import json
import os
import datetime

class AuditLogger:
    def __init__(self, log_file="data/audit_log.json"):
        self.log_file = log_file

    def log_decision(self, user_input: str, decision: dict):
        entry = {
            "timestamp": str(datetime.datetime.now()),
            "input": user_input,
            "decision": decision
        }

        data = []
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                try:
                    data = json.load(f)
                except: data = []

        data.append(entry)
        with open(self.log_file, "w") as f:
            json.dump(data, f, indent=4)
