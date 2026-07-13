import json
import os
import logging

class StateManager:
    def __init__(self, persistence_file="data/state.json"):
        self.persistence_file = persistence_file
        self.state = self.load_state()

    def load_state(self):
        if os.path.exists(self.persistence_file):
            try:
                with open(self.persistence_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Failed to load state: {e}")
        return {"decision_cache": {}, "roadmaps": {}, "user_fixes": [], "style_preferences": {}}

    def save_state(self):
        os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)
        try:
            with open(self.persistence_file, "w") as f:
                json.dump(self.state, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save state: {e}")

    def record_user_fix(self, original_code, fixed_code, feedback):
        """Records user-provided fixes for future fine-tuning/learning."""
        self.state["user_fixes"].append({
            "original": original_code,
            "fixed": fixed_code,
            "feedback": feedback
        })
        self.save_state()

    def update_decision_cache(self, key, value):
        self.state["decision_cache"][key] = value
        self.save_state()

    def get_decision_cache(self):
        return self.state.get("decision_cache", {})
