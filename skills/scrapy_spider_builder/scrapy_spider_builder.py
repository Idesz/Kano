import ollama

class ScrapySpiderBuilder:
    def execute(self, domain: str, target_data: str):
        prompt = f"Write a Scrapy spider for '{domain}' to extract '{target_data}'. Include item pipelines and middleware suggestions."
        response = ollama.generate(model="deepseek-coder", prompt=prompt)
        return response['response']
