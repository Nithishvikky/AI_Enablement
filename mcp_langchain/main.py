import asyncio
from agent import create_research_agent


async def console():
    """Console interface for the Internal Research Agent"""
    print("Initializing Internal Research Agent...")
    agent = await create_research_agent()
    print("Agent ready!\n")
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Goodbye!")
                break
            
            print("\nAgent is thinking...\n")
            result = await agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user", 
                            "content": user_input
                        }
                    ]
                }
            )
            print(f"Agent: {result['messages'][-1].content}\n")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")


if __name__ == "__main__":
    asyncio.run(console())
