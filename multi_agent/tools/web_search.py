from langchain_community.tools import DuckDuckGoSearchRun


# Initialize the search tool
search = DuckDuckGoSearchRun()


def search_web(query: str) -> str:
    """
    Search the web using DuckDuckGo
    
    Args:
        query (str): The search query
        
    Returns:
        str: Search results
    """
    try:
        results = search.run(query)
        return results
    except Exception as e:
        return f"Error performing web search: {str(e)}"


def search_news(topic: str) -> str:
    """
    Search for news on a specific topic
    
    Args:
        topic (str): The topic to search for
        
    Returns:
        str: News search results
    """
    query = f"news {topic}"
    return search_web(query)
