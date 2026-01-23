from langchain_aws import ChatBedrockConverse
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from rag_tool import create_hr_rag_tool
from web_tool import create_web_search_tool


async def create_research_agent():
    """Create and initialize the Internal Research Agent"""
    
    client = MultiServerMCPClient({
        "mcp_tool": {
            "command": "python",
            "args": ["mcp_server.py"],
            "transport": "stdio",
        }
    })
    
    # Get MCP tools automatically
    mcp_tools = await client.get_tools()

    # RAG tool
    hr_rag_tool = create_hr_rag_tool()

    # Web tool
    web_search_tool = create_web_search_tool()

    # LLM
    llm = ChatBedrockConverse(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        region_name="us-east-1"
    )

    custom_prompt = f"""
        You are an Internal Research Agent for the Presidio.
        You can use the following tools: {[t.name for t in [*mcp_tools, hr_rag_tool, web_search_tool]]}.
        Select the appropriate tool based on whether the query needs internal data, policies, or external benchmarks.
        Combine tools when necessary to produce comparative or multi-source insights.
        Never hallucinate; rely only on retrieved information.
        Clearly separate internal data from external references.
        Be concise, structured, and actionable in your responses.
        If data is missing or unclear, state limitations and suggest next steps.
    """

    # Create ReAct agent
    agent = create_agent(
        model=llm, 
        tools=[*mcp_tools, hr_rag_tool, web_search_tool],
        system_prompt=custom_prompt
    )

    return agent
