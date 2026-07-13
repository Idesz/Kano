import ollama

class HallucinationDetector:
    def __init__(self, model_router):
        self.router = model_router

    def cross_check(self, statement: str, source_context: str):
        """Asks the LLM to verify if a statement is supported by the provided context."""
        model = self.router.get_model_for_task("reasoning")
        prompt = f"""
        Context: {source_context}
        Statement: {statement}

        Is the Statement factually supported by the Context?
        Answer ONLY with 'SUPPORTED' or 'HALLUCINATION' and a 1-sentence reason.
        """
        response = ollama.generate(model=model, prompt=prompt)
        return response['response'].strip()
