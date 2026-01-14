import boto3
import json
from questions import questions
from prompts import prompts


def run_claude(prompt):

    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )

    result = json.loads(response["body"].read())
    return result

def main():
    
    with open("responses.md", "w") as f:
        f.write("# Prompt Optimization Results\n\n")
    
    
    for prompt_type, prompt_text in prompts.items():
        
        with open("responses.md", "a") as f:
            f.write(f"## {prompt_type.title()} Prompt Results\n\n")
        
        for question in questions:

            full_prompt = f"{prompt_text}\n\nUser Question: {question}"
            
            result = run_claude(full_prompt)
            response_text = result["content"][0]["text"]
            
            formatted_result = f"**Question:** `{question}`\n\n**Response:**\n```text\n{response_text}\n```\n\n---\n\n"
            
            with open("responses.md", "a") as f:
                f.write(formatted_result)
                    
    
    print("All prompts processed! Check responses.md for results.")

if __name__ == "__main__":
    main()