from mcp.server.fastmcp import FastMCP
from langchain_google_community import  GoogleDriveLoader
from dotenv import load_dotenv
import os

load_dotenv()


# Create MCP server
mcp = FastMCP("mcp_tool")


def load_docs():
    loader = GoogleDriveLoader(
        credentials_path="credentials.json",
        token_path="token.json",
        folder_id=os.getenv("FOLDER_ID"),
    )
    docs = loader.load()
    print(f"DEBUG: Loaded {len(docs)} documents from Google Drive")
    return docs

@mcp.tool()
def read_insurance_docs() -> str:
    """
    Reads and returns the complete content of all group health insurance policy documents from Google Drive.
    This tool retrieves the full text of insurance documents that can be summarized or analyzed.
    Always use this tool first when asked about insurance policies, summaries, or coverage details.

    Returns: Complete text content of all insurance documents.
    """
    docs = load_docs()
    if not docs:
        return "No insurance documents found in Google Drive."
    
    result = []
    for i, doc in enumerate(docs):
        title = doc.metadata.get("title", f"Document {i+1}")
        result.append(f"=== {title} ===\n{doc.page_content}")
    
    return "\n\n".join(result)

@mcp.tool()
def search_insurance(keyword: str) -> str:
    """
    Searches insurance policy documents for a specific keyword or term.
    Use this when looking for specific information like 'deductible', 'coverage', 'copay', etc.
    
    Args:
        keyword: The term to search for in the insurance documents
    
    Returns: List of document titles containing the keyword
    """
    docs = load_docs()
    if not docs:
        return "No insurance documents found in Google Drive."
    
    matches = []
    for i, doc in enumerate(docs):
        if keyword.lower() in doc.page_content.lower():
            title = doc.metadata.get("title", f"Document {i+1}")
            content = doc.page_content.lower()
            idx = content.find(keyword.lower())
            snippet = doc.page_content[max(0, idx-100):idx+100]
            matches.append(f"{title}: ...{snippet}...")
    
    return "\n\n".join(matches) if matches else f"No matches found for '{keyword}'."


if __name__ == "__main__":
    mcp.run(transport="stdio")