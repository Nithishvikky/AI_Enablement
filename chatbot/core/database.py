import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Tuple, Optional

class ChromaDBManager:
    """Manages ChromaDB operations for document storage and retrieval"""
    
    def __init__(self, db_path: str = "data/chroma_db", collection_name: str = "documents_collection"):
        """Initialize ChromaDB client with persistence"""
        self.db_path = db_path
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = None
        self.embedding_function = None
        
    def create_collection(self, embedding_model: str = "all-MiniLM-L6-v2"):
        """Create or get existing collection with embeddings"""
        try:
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=embedding_model
            )
            
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            
            print(f"Collection '{self.collection_name}' initialized successfully")
            return True
        except Exception as e:
            print(f"Error creating collection: {str(e)}")
            return False
    
    def add_documents_batch(self, ids: List[str], texts: List[str], metadatas: List[Dict], batch_size: int = 100):
        """Add documents to collection in batches"""
        if not self.collection:
            raise Exception("Collection not initialized. Call create_collection() first.")
        
        if not texts:
            return
        
        try:
            for i in range(0, len(texts), batch_size):
                end_idx = min(i + batch_size, len(texts))
                self.collection.add(
                    documents=texts[i:end_idx],
                    metadatas=metadatas[i:end_idx],
                    ids=ids[i:end_idx]
                )
            print(f"Successfully added {len(texts)} document chunks to collection")
        except Exception as e:
            print(f"Error adding documents to collection: {str(e)}")
    
    def semantic_search(self, query: str, n_results: int = 3) -> Dict:
        """Perform semantic search on the collection"""
        if not self.collection:
            raise Exception("Collection not initialized. Call create_collection() first.")
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Error performing semantic search: {str(e)}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def get_context_with_sources(self, results: Dict) -> Tuple[str, List[str]]:
        """Extract context and source information from search results"""
        if not results or not results.get('documents') or not results['documents'][0]:
            return "", []
        
        # Combine document chunks into a single context
        context = "\n\n".join(results['documents'][0])
        
        # Format sources with metadata
        sources = [
            f"{meta['source']} (chunk {meta['chunk']})" 
            for meta in results['metadatas'][0]
        ]
        
        return context, sources
    
    def get_collection_stats(self) -> Dict:
        """Get collection statistics"""
        if not self.collection:
            return {"error": "Collection not initialized"}
        
        try:
            count = self.collection.count()
            return {"document_count": count, "collection_name": self.collection_name}
        except Exception as e:
            return {"error": f"Error getting stats: {str(e)}"}
    
    def delete_documents(self, ids: List[str]):
        """Delete documents from collection"""
        if not self.collection:
            raise Exception("Collection not initialized")
        
        try:
            self.collection.delete(ids=ids)
            print(f"Deleted {len(ids)} documents")
        except Exception as e:
            print(f"Error deleting documents: {str(e)}")
