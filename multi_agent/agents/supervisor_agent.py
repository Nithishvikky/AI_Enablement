from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse
from models.response_model import ClassificationResponse


def create_supervisor_agent():
    """
    Create and return a Supervisor agent using LangChain's create_agent
    
    Returns:
        Agent: Configured Supervisor agent
    """
    
    # Initialize the model
    model = ChatBedrockConverse(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name="us-east-1",
        max_tokens=4096
    )
    
    system_prompt = """
    You are a classification agent. Classify the following query strictly as:
        - IT
        - FINANCE
        - OTHER

        Return ONLY one of: IT, FINANCE, or OTHER.
    """
    
    # Create the agent with prompt template
    agent = create_agent(
        model=model,
        system_prompt=system_prompt,
        response_format=ClassificationResponse
    )
    
    return agent
