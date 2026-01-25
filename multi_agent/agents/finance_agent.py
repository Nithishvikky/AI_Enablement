from langchain.agents import create_agent
from langchain_core.tools import Tool
from langchain_aws import ChatBedrockConverse
from models.response_model import SupportAgentResponse
from tools.file_rag import search_vector_db
from tools.web_search import search_web, search_news


def create_finance_agent():
    """
    Create and return a Finance agent using LangChain's create_agent
    
    Returns:
        Agent: Configured Finance agent with tools
    """
    
    # Initialize the model
    model = ChatBedrockConverse(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name="us-east-1",
        max_tokens=4096
    )
    
    # Define tools for the Finance agent
    tools = [
        Tool(
            name="search_finance_docs_rag",
            func=search_vector_db,
            description="Find Finance documentation containing budget planning, financial reporting, cost analysis, revenue forecasting, and risk management information"
        ),
        Tool(
            name="search_web",
            func=search_web,
            description="Search the web for financial information, market trends, and economic news"
        ),
        Tool(
            name="search_news",
            func=search_news,
            description="Search for news related to finance, markets, and economic updates"
        )
    ]
    
    # System prompt for Finance agent
    system_prompt = """
    You are a Finance support agent.
    Use internal finance docs first.
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
