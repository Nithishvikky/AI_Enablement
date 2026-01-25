from langchain.agents import create_agent
from langchain_core.tools import Tool
from langchain_aws import ChatBedrockConverse
from models.response_model import SupportAgentResponse
from tools.file_rag import search_vector_db
from tools.web_search import search_web, search_news


def create_it_agent():
    """
    Create and return an IT agent using LangChain's create_agent
    
    Returns:
        Agent: Configured IT agent with tools
    """
    
    # Initialize the model
    model = ChatBedrockConverse(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name="us-east-1",
        max_tokens=4096
    )
    
    # Define tools for the IT agent
    tools = [
        Tool(
            name="search_it_docs_rag",
            func=search_vector_db,
            description="Find IT documentation containing system architecture, network configuration, database management, security protocols, and disaster recovery information"
        ),
        Tool(
            name="search_web",
            func=search_web,
            description="Search the web for IT-related information, best practices, and current technologies"
        ),
        Tool(
            name="search_news",
            func=search_news,
            description="Search for news related to IT topics and technology updates"
        )
    ]
    
    # System prompt for IT agent
    system_prompt = """
    You are an IT support agent.
    Use internal IT docs first.
    If insufficient, search the web.

    Always return your answer using the structured response format provided.
    """
    
    # Create and return the agent
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        response_format= SupportAgentResponse
    )
    
    return agent
