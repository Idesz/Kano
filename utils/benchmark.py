import time
import ollama

def benchmark_model(model_name="llama3"):
    prompt = "Write a short poem about a rainy day in Budapest."
    start_time = time.time()
    response = ollama.generate(model=model_name, prompt=prompt)
    end_time = time.time()

    tokens = len(response['response'].split()) # Rough estimate
    duration = end_time - start_time
    tokens_per_sec = tokens / duration if duration > 0 else 0

    return {
        "model": model_name,
        "tokens_per_sec": tokens_per_sec,
        "recommendation": "Use 4-bit quantization for < 10 t/s" if tokens_per_sec < 10 else "Optimal performance"
    }
