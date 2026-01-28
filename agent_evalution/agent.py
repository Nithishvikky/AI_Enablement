from langchain.agents import create_agent
from langchain_core.tools import Tool
from langchain_aws import ChatBedrockConverse
from tools import calculator_tool, text_length_tool, uppercase_tool


def create_agent_function():
    """
    Create and return a Bedrock agent with NeMo Guardrails integration
    
    Returns:
        RunnableRails: Configured Bedrock agent with guardrails and tools
    """

    # Initialize the model
    model = ChatBedrockConverse(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name="us-east-1",
        max_tokens=4096,
    )
    
    # Define tools for the agent
    tools = [
        Tool(
            name="calculator",
            func=calculator_tool,
            description="Perform mathematical calculations. Input should be a mathematical expression like '25 * 4 + 10'",
        ),
        Tool(
            name="text_length",
            func=text_length_tool,
            description="Count the number of characters in a given text string",
        ),
        Tool(
            name="uppercase",
            func=uppercase_tool,
            description="Convert text to uppercase letters",
        )
    ]
    
    # System prompt for the agent
    system_prompt = """
    You are a helpful AI assistant with access to various tools.
    You must follow safety guidelines and comply with all input validation rules.
    
    Available tools:
    - calculator: For mathematical calculations
    - text_length: To count characters in text
    - uppercase: To convert text to uppercase
    
    Do not explain your reasoning.
    Always call tools silently.
    Strictly Return only the final result.
    """

    # Create the base agent
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
    )
    
    return agent