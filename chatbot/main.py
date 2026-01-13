import os
import sys
from core.database import ChromaDBManager
from core.ai_client import BedrockAIClient
from core.conversation import ConversationManager
from core.text_processor import TextProcessor

class ChatbotConsole:
    """Console interface for the RAG chatbot"""
    
    def __init__(self):
        """Initialize the chatbot console"""
        print("Initializing RAG Chatbot...")
        
        # Initialize components
        self.db_manager = ChromaDBManager()
        self.ai_client = BedrockAIClient()
        self.conversation_manager = ConversationManager()
        self.session_id = None
        
        # Setup
        self.setup()
    
    def setup(self):
        """Setup the chatbot components"""
        # Initialize database
        if not self.db_manager.create_collection():
            print("Failed to initialize database. Exiting.")
            sys.exit(1)
        
        # Test AI connection
        if not self.ai_client.test_connection():
            print("Warning: AI client connection test failed. Responses may not work.")
        
        # Create conversation session
        self.session_id = self.conversation_manager.create_session()
        print("Chatbot initialized successfully!")
    
    def load_documents(self, folder_path: str):
        """Load documents from a folder"""
        try:
            if not os.path.exists(folder_path):
                print(f"Error: Folder '{folder_path}' not found.")
                return
            
            print(f"Loading documents from '{folder_path}'...")
            ids, texts, metadatas = TextProcessor.process_multiple_documents(folder_path)
            
            if not texts:
                print("No supported documents found in the folder.")
                return
            
            self.db_manager.add_documents_batch(ids, texts, metadatas)
            print(f"Successfully loaded {len(texts)} document chunks.")
            
        except Exception as e:
            print(f"Error loading documents: {str(e)}")
    
    def process_query(self, query: str):
        """Process a user query and return response"""
        try:
            # Get conversation history
            conversation_history = self.conversation_manager.format_history_for_prompt(self.session_id)
            
            # Contextualize query if needed
            contextualized_query = self.ai_client.contextualize_query(query, conversation_history)
            
            # Perform semantic search
            results = self.db_manager.semantic_search(contextualized_query, n_results=3)
            context, sources = self.db_manager.get_context_with_sources(results)
            
            # Generate response
            response = self.ai_client.generate_response(query, context, conversation_history)
            
            # Add to conversation history
            self.conversation_manager.add_message(self.session_id, "user", query)
            self.conversation_manager.add_message(self.session_id, "assistant", response)
            
            return response, sources
            
        except Exception as e:
            return f"Error processing query: {str(e)}", []
    
    def show_help(self):
        """Show help message"""
        help_text = """
            Available Commands:
            /load <folder_path>  - Load documents from a folder
            /stats              - Show database statistics
            /clear              - Clear conversation history
            /help               - Show this help message
            /exit               - Exit the chatbot

            Simply type your question to chat with the bot.
        """
        print(help_text)
    
    def show_stats(self):
        """Show database statistics"""
        stats = self.db_manager.get_collection_stats()
        print(f"Database Statistics: {stats}")
    
    def run(self):
        """Run the console interface"""
        print("\n" + "="*50)
        print("RAG Chatbot Console")
        print("="*50)
        print("Type '/help' for commands or just start chatting!")
        print("Type '/exit' to quit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    command_parts = user_input.split(' ', 1)
                    command = command_parts[0].lower()
                    
                    if command == '/exit':
                        print("Goodbye!")
                        break
                    elif command == '/help':
                        self.show_help()
                    elif command == '/stats':
                        self.show_stats()
                    elif command == '/clear':
                        self.conversation_manager.clear_session(self.session_id)
                        print("Conversation history cleared.")
                    elif command == '/load':
                        if len(command_parts) > 1:
                            self.load_documents(command_parts[1])
                        else:
                            print("Usage: /load <folder_path>")
                    else:
                        print(f"Unknown command: {command}. Type '/help' for available commands.")
                    
                    continue
                
                # Process regular query
                print("Bot: ", end="", flush=True)
                response, sources = self.process_query(user_input)
                print(response)
                
                if sources:
                    print(f"\nSources: {', '.join(sources)}")
                print()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

def main():
    """Main entry point"""
    chatbot = ChatbotConsole()
    chatbot.run()

if __name__ == "__main__":
    main()
