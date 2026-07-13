import os
import json
import importlib.util
import logging
import multiprocessing

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

                    module_file = os.path.join(skill_path, f"{skill_name}.py")
                    if os.path.exists(module_file):
                        # Store metadata and path, load class on demand
                        self.skills[skill_name] = {
                            "path": module_file,
                            "class_name": metadata.get("class_name", skill_name.replace("_", " ").title().replace(" ", "")),
                            "metadata": metadata
                        }
                except Exception as e:
                    logging.error(f"Failed to index skill {skill_name}: {e}")

    def execute_skill_isolated(self, skill_name, **kwargs):
        """Executes a skill in a separate process to prevent crashes."""
        if skill_name not in self.skills:
            return f"Skill {skill_name} not found."

        # Process isolation using multiprocessing
        result_queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=self._run_skill_process, args=(skill_name, kwargs, result_queue))
        p.start()
        p.join(timeout=60) # Skill timeout

        if p.is_alive():
            p.terminate()
            return f"Skill {skill_name} timed out."

        return result_queue.get() if not result_queue.empty() else "Skill execution failed."

    def _run_skill_process(self, skill_name, kwargs, queue):
        try:
            skill_info = self.skills[skill_name]
            spec = importlib.util.spec_from_file_location(skill_name, skill_info["path"])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            skill_class = getattr(module, skill_info["class_name"])
            instance = skill_class()
            result = instance.execute(**kwargs)
            queue.put(result)
        except Exception as e:
            queue.put(f"Process Error: {e}")

    def get_skill(self, name):
        return self.skills.get(name)

    def list_skills(self):
        return [{"name": name, "description": data["metadata"].get("description")} for name, data in self.skills.items()]
