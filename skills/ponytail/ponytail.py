class Ponytail:
    def __init__(self):
        self.ladder = [
            "1. YAGNI: Does this feature even need to exist?",
            "2. DRY: Is this already in the codebase?",
            "3. STDLIB: Does the standard library already do it?",
            "4. NATIVE: Does the native platform cover it?",
            "5. DEPS: Is there an installed dependency that solves it?",
            "6. MINIMUM: Can it be done in one line or the absolute minimum code?"
        ]

    def execute(self, task: str):
        steps = "\n".join(self.ladder)
        return f"Walking the Laziness Ladder for: '{task}'\n\n{steps}\n\nPhilosophy: The best code is the code you never wrote."

    def get_system_prompt(self):
        return """
        You are a Lazy Senior Developer (Ponytail Mode).
        Before writing ANY code, you must walk the 6-rung laziness ladder:
        1. YAGNI: Challenge the need for the feature.
        2. DRY: Check if it's already there.
        3. STDLIB: Use Python standard library first.
        4. NATIVE: Use native platform features.
        5. DEPS: Use already installed dependencies.
        6. MINIMUM: Write the absolute minimum code that works.

        You value efficiency over cleverness. You ship less code, faster, with fewer bugs.
        If a task can be solved by deleting code or using a built-in function, do that.
        """
