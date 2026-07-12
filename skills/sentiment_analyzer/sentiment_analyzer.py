import ollama

class SentimentAnalyzer:
    def execute(self, text: str):
        prompt = f"Analyze the sentiment of the following text and provide a score/summary (Positive/Negative/Neutral).\nText:\n{text}"
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
