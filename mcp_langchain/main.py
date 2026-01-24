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

            # Extract and display tools used and response time
            tools_used = set()
            latency_ms = 0
            
            for message in result.get('messages', []):
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    for tool_call in message.tool_calls:
                        if isinstance(tool_call, dict):
                            tools_used.add(tool_call.get('name', 'Unknown'))
                        else:
                            tools_used.add(str(tool_call.name))
                
                if hasattr(message, 'response_metadata') and message.response_metadata:
                    metadata = message.response_metadata
                    if 'metrics' in metadata and metadata['metrics']:
                        latency_ms = metadata['metrics'].get('latencyMs', [0])[0]
            
            if tools_used:
                print(f"Tools used: {', '.join(sorted(tools_used))}")
            
            if latency_ms:
                print(f"Response time: {latency_ms}ms")

            print(f"\n\n----- Agent Response ----- \n{result['messages'][-1].content}\n")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")


if __name__ == "__main__":
    asyncio.run(console())
