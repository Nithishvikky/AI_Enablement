import boto3
import json
from typing import List, Dict

class BedrockAIClient:
    """Handles AWS Bedrock AI interactions"""
    
    def __init__(self, region_name: str = "us-east-1"):
        """Initialize Bedrock client"""
        try:
            self.client = boto3.client("bedrock-runtime", region_name=region_name)
            self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        except Exception as e:
            print(f"Error initializing Bedrock client: {str(e)}")
            self.client = None
    
    def generate_response(self, query: str, context: str, conversation_history: str = "") -> str:
        """Generate a response using AWS Bedrock Claude"""
        if not self.client:
            return "Error: Bedrock client not initialized"
        
        prompt = self.get_prompt(context, conversation_history, query)
        
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2048,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                })
            )
            
            result = json.loads(response["body"].read())
            return result["content"][0]["text"]
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def contextualize_query(self, query: str, conversation_history: str) -> str:
        """Convert follow-up questions into standalone queries"""
        if not conversation_history.strip():
            return query
        
        contextualize_prompt = """Given a chat history and the latest user question 
        which might reference context in the chat history, formulate a standalone 
        question which can be understood without the chat history. Do NOT answer 
        the question, just reformulate it if needed and otherwise return it as is."""
        
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [
                        {"role": "user", "content": f"{contextualize_prompt}\n\nChat history:\n{conversation_history}\n\nQuestion:\n{query}"}
                    ]
                })
            )
            result = json.loads(response["body"].read())
            return result["content"][0]["text"]
        except Exception as e:
            print(f"Error contextualizing query: {str(e)}")
            return query
    
    def get_prompt(self, context: str, conversation_history: str, query: str) -> str:
        """Generate a prompt combining context, history, and query"""
        prompt = f"""Based on the following context and conversation history, 
        please provide a relevant and contextual response. If the answer cannot 
        be derived from the context, only use the conversation history or say 
        "I cannot answer this based on the provided information."

        Context from documents:
        {context}

        Previous conversation:
        {conversation_history}

        Human: {query}

        Assistant:"""
        
        return prompt
    
    def test_connection(self) -> bool:
        """Test if Bedrock connection is working"""
        if not self.client:
            return False
        
        try:
            # Simple test query
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Hello"}]
                })
            )
            return True
        except Exception as e:
            print(f"Bedrock connection test failed: {str(e)}")
            return False
