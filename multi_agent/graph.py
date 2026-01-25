from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from agents.supervisor_agent import create_supervisor_agent
from agents.it_agent import create_it_agent
from agents.finance_agent import create_finance_agent
from models.response_model import SupportAgentResponse


class State(TypedDict):
    """State for the multi-agent router"""
    query: str
    classification: str
    response: str


def supervisor_node(state: State) -> State:
    """
    Supervisor node - Classifies the query as IT or FINANCE using structured output
    
    Args:
        state (State): Current state
        
    Returns:
        State: Updated state with classification
    """
    supervisor = create_supervisor_agent()
    response = supervisor.invoke(
        {
            "messages": [
                {
                    "role": "user", 
                    "content": state["query"]
                }
            ]
        }
    )
    
    # Extract structured response
    structured_response = response.get('structured_response')
    
    if structured_response:
        # Extract classification from Pydantic model
        state['classification'] = structured_response.classification
    
    return state


def it_node(state: State) -> State:
    """
    IT Agent node - Handles IT-related queries
    
    Args:
        state (State): Current state
        
    Returns:
        State: Updated state with IT agent response
    """
    it_agent = create_it_agent()
    response = it_agent.invoke(
        {
            "messages": [
                {
                    "role": "user", 
                    "content": state["query"]
                }
            ]
        }
    )

    # Extract structured response
    structured_response = response.get('structured_response')
    
    if structured_response:
        state['response'] = structured_response
    
    return state


def finance_node(state: State) -> State:
    """
    Finance Agent node - Handles Finance-related queries
    
    Args:
        state (State): Current state
        
    Returns:
        State: Updated state with Finance agent response
    """
    finance_agent = create_finance_agent()
    response = finance_agent.invoke(
        {
            "messages": [
                {
                    "role": "user", 
                    "content": state["query"]
                }
            ]
        }
    )

    # Extract structured response
    structured_response = response.get('structured_response')
    
    if structured_response:
        state['response'] = structured_response
    
    return state


def other_node(state: State) -> State:
    """
    Other node - Handles non-related queries
    
    Args:
        state (State): Current state
        
    Returns:
        State: Updated state for other response
    """
    state['response'] = SupportAgentResponse(
        answer="Sorry, I can only assist with IT or Finance related queries at the moment.",
        sources=[],
        tools_used=[],
        confidence=1.0,
        latency_ms=0.0,
        notes="Query outside supported domains"
    )
    return state


def route_query(state: State) -> Literal["IT", "FINANCE", "OTHER"]:
    """
    Routing function - Determines which agent should handle the query
    
    Args:
        state (State): Current state with classification
        
    Returns:
        str: Route to IT or FINANCE agent
    """
    classification = state.get('classification', '').strip().upper()
    
    if 'IT' in classification:
        return "IT"
    elif 'FINANCE' in classification:
        return "FINANCE"
    else:
        return "OTHER"


def create_router_graph():
    """
    Create and compile the router graph
    
    Returns:
        Compiled LangGraph that routes queries to appropriate agents
    """
    
    # Create the state graph
    graph = StateGraph(State)
    
    # Add nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("IT", it_node)
    graph.add_node("FINANCE", finance_node)
    graph.add_node("OTHER", other_node)
    
    # Add entry point
    graph.set_entry_point("supervisor")
    
    # Add edges with conditional routing
    graph.add_conditional_edges(
        "supervisor",
        route_query,
        {
            "IT": "IT",
            "FINANCE": "FINANCE",
            "OTHER": "OTHER"
        }
    )
    
    # Add edges to end
    graph.add_edge("IT", END)
    graph.add_edge("FINANCE", END)
    graph.add_edge("OTHER", END)
    
    # Compile the graph
    compiled_graph = graph.compile()
    
    return compiled_graph
