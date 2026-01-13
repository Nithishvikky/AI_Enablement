import time
import json
import requests
import os
from dotenv import load_dotenv
import boto3

load_dotenv() # Load .env file


OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
GEMINI_API_BASE_URL = os.getenv("GEMINI_API_BASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODELS_TO_EVALUATE = [
    {"name": "Gemini Flash", "type": "google", "model_id": "gemini-2.5-flash"},
    {"name": "Claude Sonnet (Bedrock)", "type": "anthropic", "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0"},
    {"name": "DeepSeek R1 7b", "type": "ollama", "model_id": "deepseek-r1:7b"}
]

TASK_PROMPTS = {
    "application_development": "Write a JavaScript function that takes an array of numbers and returns the maximum value. Handle empty arrays by returning null. Output only code. Max 300 characters.",
    "automation_scripts": "Write a Bash script that counts the number of .jpg files in the current directory and prints the count. Handle empty directories. Output only code. Max 300 characters.",
    "sql_generation": "Given a table orders(order_id, customer_id, total_amount), write SQL to find the top 5 highest orders by total_amount. Output only the query. Max 300 characters."
}

def query_gemini_model(model_id, prompt_text):
    try:
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt_text
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": 2048
            }
        }

        gemini_api_url = f"{GEMINI_API_BASE_URL}/{model_id}:generateContent"
        url = f"{gemini_api_url}?key={GEMINI_API_KEY}"

        response = requests.post(url, json=payload, timeout=60)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        return f"Gemini API Error: {str(e)}"
    except KeyError:
         return "Gemini API Error: Malformed JSON response from Gemini."

def query_anthropic_model(model_id, prompt_text):
    try:
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name="us-east-1",
        )

        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            accept='application/json',
            contentType='application/json',
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2048,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt_text}]
                    }
                ]
            })
        )

        response_body = json.loads(response.get('body').read())

        if response_body.get("content") and isinstance(response_body["content"], list) and len(response_body["content"]) > 0:
            return response_body["content"][0].get("text")
        else:
            return "Error: Could not parse response from Bedrock. Check response structure."

    except Exception as e:
        return f"AWS Bedrock (Anthropic) API Error: {str(e)}"

def query_ollama_model(model_id, prompt_text):
    """Sends a prompt to a local Ollama API and returns the response."""
    payload = {"model": model_id, "prompt": prompt_text, "stream": False}
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "Error: 'response' key not found in Ollama output.")
    except requests.exceptions.RequestException as e:
        return f"Ollama API Error: {str(e)}"
    except KeyError:
         return "Ollama API Error: Malformed JSON response from Ollama."


def save_results_to_markdown(results: list) -> str:
    """Saves the results to a Markdown file"""
    markdown = "# Model Comparison Results\n\n"
    for result in results:
        markdown += f"## Model: {result['model_name']}\n\n"
        markdown += f"### Task: {result['task_description']}\n\n"
        markdown += f"**Latency:** {result['latency_seconds']}\n\n"
        markdown += f"**Prompt:**\n{result['prompt_text']}\n\n\n"
        markdown += f"**Response:**\n{result['response_text']}\n\n"
        markdown += "---\n\n"
    return markdown


if __name__ == "__main__":
    print("Starting AI Model Evaluation Script...")
    evaluation_results = []
    
    for model_config in MODELS_TO_EVALUATE:
        model_name = model_config["name"]
        model_type = model_config["type"]
        model_id = model_config["model_id"]

        print(f"\n--- Evaluating Model: {model_name} ({model_id}) ---")

        for task_name, task_prompt in TASK_PROMPTS.items():

            print(f"    Running Task: {task_name}")

            start_time = time.time()
            response_text = ""
            error_message = None

            try:
                if model_type == "anthropic":
                    response_text = query_anthropic_model(model_id, task_prompt)
                elif model_type == "google":
                    response_text = query_gemini_model(model_id, task_prompt)
                elif model_type == "ollama":
                    response_text = query_ollama_model(model_id, task_prompt)
                else:
                    raise ValueError(f"Unknown model type: {model_type}")
            except Exception as e:
                error_message = str(e)
                response_text = f"ERROR DURING API CALL: {e}"
                print(f"      ERROR: {e}")

            end_time = time.time()
            latency_seconds = end_time - start_time

            result_entry = {
                    "model_name": model_name,
                    "model_id": model_id,
                    "task_description": task_name,
                    "prompt_text": task_prompt,
                    "response_text": response_text,
                    "latency_seconds": round(latency_seconds, 3),
                    "error": error_message,
                }
            evaluation_results.append(result_entry)
            print(f"      Latency: {latency_seconds:.3f}s")
    # Save results to a Markdown file
    with open("results.md", "w") as f:
        f.write(save_results_to_markdown(evaluation_results))
    print("\n--- Evaluation Collection Complete ---")
