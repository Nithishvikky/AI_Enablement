# Multi-Agent Support System

## Overview

This is a multi-agent support system built with LangGraph that intelligently routes user queries to specialized agents. The system uses AWS Bedrock Claude 3.5 Sonnet model and provides structured responses for IT and Finance related queries through a conversational interface.

## Folder Structure

```
multi_agent/
├── main.py                     # Entry point and interactive chat console
├── graph.py                    # LangGraph router implementation             
├── agents/       
│   ├── supervisor_agent.py     # Classification agent
│   ├── it_agent.py             # IT support specialist
│   └── finance_agent.py        # Finance support specialist
├── models/
│   └── response_model.py       # Unified response format
├── tools/
│   ├── file_rag.py             # Vector database search for internal docs
│   └── web_search.py           # Web and news search functionality
└── rag/
    └── rag_index.py            # Document indexing for vector database
```

## Agents Overview

**Supervisor Agent**: Classifies incoming queries as IT, FINANCE, or OTHER using structured output with confidence scoring and reasoning.
Acts as the entry point router that determines which specialized agent should handle the user's request.

**IT Agent**: Handles technical support queries related to system architecture, network configuration, database management, and security protocols.
Uses internal IT documentation via RAG and can fallback to web search for current technology information and best practices.

**Finance Agent**: Processes financial queries including budgeting, compliance, reporting, and financial analysis using internal finance documents.
Leverages RAG-based document search and web resources to provide accurate financial guidance and regulatory information.

## Response Format

All agents return responses using the `SupportAgentResponse` Pydantic model for consistency and structure.
The format includes answer, sources, tools_used, confidence score, latency_ms, and optional notes fields.

```python
    answer: str -> "Answer to the user query"
    sources: List[str] -> "Internal docs or web URLs"
    tools_used: List[str] -> "List of tools invoked to generate the answer"
    confidence: float -> "Confidence in the answer (0.0 to 1.0)"
    latency_ms: float -> "Time taken by the agent in milliseconds"
    notes: Optional[str] -> "Optional notes, assumptions, or compliance remarks"
```

## Tools Overview

**File RAG Tool**: Searches the Chroma vector database containing indexed internal documents using HuggingFace embeddings for semantic similarity.
**Web Search Tools**: Provides web search and news search capabilities to supplement internal knowledge with current information when needed.

## Router Pattern in LangGraph

The routing system follows a conditional state graph pattern where queries flow through multiple stages:
1. **Entry Point**: All queries start at the supervisor node for classification
2. **Classification Stage**: Supervisor agent analyzes the query and assigns IT, FINANCE, or OTHER classification
3. **Conditional Routing**: Based on classification, the graph routes to the appropriate specialist agent node
4. **Agent Processing**: Selected agent processes the query using available tools and returns structured response
5. **Termination**: All agent nodes connect to END, completing the workflow with the final response
6. **State Management**: The `State` TypedDict maintains query, classification, and response throughout the graph execution

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Configure AWS credentials and environment variables in `.env` file
3. Run the interactive chat: `python main.py`
4. Type queries and receive routed responses from specialized agents
