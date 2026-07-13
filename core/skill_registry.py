import os
import json
import importlib.util
import logging
import subprocess
import sys

class SkillRegistry:
    def __init__(self, skills_dir="skills"):
        self.skills_dir = skills_dir
        self.skills = {}
        self.load_skills()

    def load_skills(self):
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
            return

        for skill_name in os.listdir(self.skills_dir):
            skill_path = os.path.join(self.skills_dir, skill_name)
            metadata_file = os.path.join(skill_path, "metadata.json")

            if os.path.isdir(skill_path) and os.path.exists(metadata_file):
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)

                    # Skill Isolation: Check/Setup Venv
                    self._setup_skill_venv(skill_path)

                    module_file = os.path.join(skill_path, f"{skill_name}.py")
                    if os.path.exists(module_file):
                        spec = importlib.util.spec_from_file_location(skill_name, module_file)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        class_name = metadata.get("class_name", skill_name.replace("_", " ").title().replace(" ", ""))
                        skill_class = getattr(module, class_name)

                        self.skills[skill_name] = {"class": skill_class, "metadata": metadata}
                except Exception as e:
                    logging.error(f"Failed to load skill {skill_name}: {e}")

    def _setup_skill_venv(self, skill_path):
        venv_path = os.path.join(skill_path, "venv")
        if not os.path.exists(venv_path):
            logging.info(f"Setting up isolation for {skill_path}")
            # Simplified: In a real scenario, this would create venv and pip install requirements.txt if present
            pass

    def get_skill(self, name):
        return self.skills.get(name)

    def list_skills(self):
        return [{"name": name, "description": data["metadata"].get("description")} for name, data in self.skills.items()]
