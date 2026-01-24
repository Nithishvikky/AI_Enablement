# Internal Research Agent

An intelligent agent that combines multiple data sources to provide comprehensive insights about HR policies, benefits, compliance, and industry benchmarks.

## Agent Overview

The **Internal Research Agent** is a ReAct-based AI assistant powered by Claude 3.5 Sonnet that intelligently selects and combines tools to answer complex organizational questions. It:
- Analyzes internal HR policies and benefits documentation
- Searches current industry standards and regulations
- Provides compliance recommendations based on internal policies vs. best practices
- Separates internal data from external references for clarity

## Architecture

```
main.py (Console Interface)
    ↓
agent.py (Agent Creation)
    ↓
    ├── MCP Server (mcp_server.py)
    │   ├── read_insurance_docs
    │   └── search_insurance
    │
    ├── RAG Tools (rag_tool.py, rag_index.py)
    │   └── search_hr_policy
    │
    └── Web Search (web_tool.py)
        └── tavily_search

Claude 3.5 Sonnet (LLM)
```

## Integration Details

### 1. **MCP (Model Context Protocol) Server**
- **File:** `mcp_server.py`
- **Connection:** Runs as stdio transport subprocess
- **Purpose:** Provides structured access to Google Drive documents (insurance policies)
- **Tools:** Insurance document reading and searching

### 2. **RAG (Retrieval Augmented Generation)**
- **Files:** `rag_tool.py`, `rag_index.py`
- **Vector Database:** Chroma (stored in `./vector_db/`)
- **Purpose:** Enables semantic search over local HR documentation
- **Process:** Documents are embedded and stored, then retrieved based on query similarity

### 3. **Web Search Integration**
- **File:** `web_tool.py`
- **Provider:** Tavily Search API
- **Purpose:** Fetches current market data, regulations, and industry benchmarks
- **Depth:** Advanced search with context-aware results

### 4. **LLM Integration**
- **Model:** Claude 3.5 Sonnet via AWS Bedrock
- **Region:** us-east-1
- **Role:** Decides which tools to use and synthesizes information

## Data Flow

1. **User Query** → Console Input
2. **Agent Analysis** → Determines required tools
3. **Parallel Tool Execution:**
   - MCP Server → Fetches insurance docs
   - RAG Search → Queries local HR policies
   - Web Search → Gets market benchmarks
4. **Information Synthesis** → Claude combines results
5. **Response Display** → Shows answer with metadata

## Available Tools

1. **read_insurance_docs** (MCP Tool)
2. **search_insurance** (MCP Tool)
3. **search_hr_policy** (RAG Tool)
4. **tavily_search** (Web Search Tool)