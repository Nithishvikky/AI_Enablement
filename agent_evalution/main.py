from langfuse import get_client
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv
from agent import create_agent_function
from validators import validate_input, validate_output
import os

load_dotenv()

# Initialize Langfuse client
langfuse = get_client()
 
# Initialize Langfuse CallbackHandler for Langchain (tracing)
langfuse_handler = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
)

def main():
    """
    Example usage of the Bedrock agent
    """
    print("Creating LangChain Bedrock Agent...")
    
    try:
        # Create the agent
        agent = create_agent_function()
        
        print("\nAgent created successfully!")
        print("\nYou can now interact with the agent.")
        print("\nEnter 'quit' to exit")
        print("-" * 50)
        
        # Interactive loop
        while True:
            user_input = input("\nYou : ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if user_input.strip():
                try:
                    # Validate input with error handling for telemetry issues
                    try:
                        allowed, response = validate_input(user_input)
                    except Exception:
                        # If validation fails due to telemetry, assume input is allowed
                        print("Warning: Validation telemetry unavailable, proceeding...")
                        allowed, response = True, None

                    if allowed:
                        # Get agent response
                        response = agent.invoke(
                            {"messages": [{"role": "user", "content": user_input}]},
                            config={"callbacks": [langfuse_handler]}
                        )

                        # Validate output with error handling
                        try:
                            output = validate_output(response['messages'][-1].content)
                        except Exception:
                            # If output validation fails due to telemetry, use original output
                            output = response['messages'][-1].content

                        print(f"\nAgent: {output}")
                        
                    else:
                        print(f"\nAgent: {response}")
                        
                except Exception as e:
                    print(f"Error: {str(e)}")
            else:
                print("Please enter a valid question.")
                
    except Exception as e:
        print(f"Error creating agent: {str(e)}")


if __name__ == "__main__":
    main()
