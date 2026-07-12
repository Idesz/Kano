import ollama

class YTTranscriptSummarizer:
    def execute(self, transcript: str):
        prompt = f"Analyze and summarize the following YouTube transcript into key insights and action items.\nTranscript:\n{transcript}"
        response = ollama.generate(model="llama3", prompt=prompt)
        return response['response']
