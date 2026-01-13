import boto3
import json


bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

with open("docs/standards.txt") as f:
    coding_rules = f.read()

with open("docs/schema_rules.txt") as f:
    schema_rules = f.read()

question = """
Write a Python function that creates a user and logs the request payload.
"""

prompt = f"""
You must strictly follow ALL rules in the CONTEXT.
If a request violates any rule, you must refuse and explain why.
If information is missing, say "Not specified in provided documents".

CONTEXT:

--- CODING STANDARDS ---
{coding_rules}

--- SCHEMA RULES ---
{schema_rules}

QUESTION:
{question}
"""

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
final_result = f"## Model Response\n\n**Response:**\n{result["content"][0]["text"]}"
# Save results to a Markdown file
with open("results.md", "w") as f:
    f.write(final_result)

