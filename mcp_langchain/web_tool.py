from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os

load_dotenv()

def create_web_search_tool():
    tool = TavilySearch(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
        tavily_api_key=os.getenv("TAVILY_API_KEY")
    )

    tool.description = (
        "Use this tool when information requires current data such as "
        "market trends, salary benchmarks, regulations, compliance updates, or industry news."
    )

    return tool