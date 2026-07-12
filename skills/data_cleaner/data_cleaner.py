import ollama

class DataCleaner:
    def execute(self, data_description: str):
        prompt = f"Write a Python script using Pandas to clean and preprocess data described as: {data_description}. Handle missing values, outliers, and type conversions."
        response = ollama.generate(model="deepseek-coder", prompt=prompt)
        return response['response']
