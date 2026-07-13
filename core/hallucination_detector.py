import ollama

class HallucinationDetector:
    def __init__(self, model_router):
        self.router = model_router

    def cross_check(self, statement: str, source_context: str, verification_model: str = None):
        """Asks a potentially larger/different model to verify the output."""
        # Use provided model or fallback to reasoning model
        model = verification_model or self.router.get_model_for_task("reasoning")

        prompt = f"""
        Verification Request:
        Context: {source_context}
        Candidate Statement: {statement}

        Check if the statement is factually grounded in the context.
        Return JSON: {{"is_hallucination": true/false, "reason": "..."}}
        """
        try:
            response = ollama.generate(model=model, prompt=prompt, format="json")
            return response['response']
        except Exception as e:
            return f"Error during verification: {e}"
