from graph import create_router_graph
from typing import Dict
from models.response_model import SupportAgentResponse


def invoke_router(query: str) -> Dict:
    """
    Invoke the router with a query
    
    Args:
        query (str): User query
        
    Returns:
        dict: Router response with classification and structured answer
    """
    router = create_router_graph()
    
    # Initial state
    initial_state = {
        "query": query,
        "classification": "",
        "response": None
    }
    
    # Execute the graph
    result = router.invoke(initial_state)
    
    return result


def main():
    """Interactive Chat Console for Multi-Agent Router"""

    print("=" * 80)
    print("MULTI-AGENT SUPPORT SYSTEM (LangGraph)")
    print("Type 'exit' to quit")
    print("=" * 80)

    while True:
        try:
            query = input("\nYou: ").strip()

            if query.lower() in ["exit", "quit"]:
                print("\nExiting support system. Goodbye!")
                break

            result = invoke_router(query)

            classification = result.get("classification", "Unknown")
            response_data = result.get("response")

            print("\n" + "-" * 80)
            print(f"Routed To  : {classification}")

            if isinstance(response_data, SupportAgentResponse):
                print(f"\nResponse   : \n\n{response_data.answer}\n{response_data.notes}\n")
                print(f"Latency    : {response_data.latency_ms:.2f} ms")
                print(f"Confidence : {response_data.confidence}")
                print(f"Sources    : {', '.join(response_data.sources)}")
                print(f"Tools Used : {', '.join(response_data.tools_used)}")
            else:
                print("Answer     :", response_data)

            print("-" * 80)

        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting support system.")
            break

        except Exception as e:
            print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
