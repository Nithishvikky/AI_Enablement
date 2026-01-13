import uuid
from datetime import datetime
from typing import Dict, List

class ConversationManager:
    """Manages conversation sessions and history"""
    
    def __init__(self):
        """Initialize conversation manager"""
        self.conversations = {}
    
    def create_session(self) -> str:
        """Create a new conversation session"""
        session_id = str(uuid.uuid4())
        self.conversations[session_id] = []
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to the conversation history"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_conversation_history(self, session_id: str, max_messages: int = None) -> List[Dict]:
        """Get conversation history for a session"""
        if session_id not in self.conversations:
            return []
        
        history = self.conversations[session_id]
        if max_messages:
            history = history[-max_messages:]
        
        return history
    
    def format_history_for_prompt(self, session_id: str, max_messages: int = 5) -> str:
        """Format conversation history for inclusion in prompts"""
        history = self.get_conversation_history(session_id, max_messages)
        formatted_history = ""
        
        for msg in history:
            role = "Human" if msg["role"] == "user" else "Assistant"
            formatted_history += f"{role}: {msg['content']}\n\n"
        
        return formatted_history.strip()
    
    def clear_session(self, session_id: str):
        """Clear conversation history for a session"""
        if session_id in self.conversations:
            self.conversations[session_id] = []
    
    def delete_session(self, session_id: str):
        """Delete a conversation session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
