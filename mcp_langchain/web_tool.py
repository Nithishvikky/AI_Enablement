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
        "Web search tool for retrieving current and latest publicly available information from the internet. "
        "Use this when user asks about: current year, latest, recent, or 2025/2026 data. "
        "Best for: industry salary benchmarks, current labor law regulations, recent compliance standards, "
        "latest HR best practices, current employee benefits trends, and recent competitive compensation analysis. "
        "Interprets 'current' and 'latest' as the most recent information available (typically up to current date). "
        "For questions mentioning current year or 'latest', this tool will search for the most recent data available. "
        "Note: Cannot predict actual future data beyond what is currently published."
    )

    return tool