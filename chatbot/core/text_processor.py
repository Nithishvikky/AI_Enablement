from typing import List, Dict, Tuple
import os

from .document_loader import DocumentLoader

class TextProcessor:
    """Handles text processing and chunking operations"""
    
    @staticmethod
    def split_text(text: str, chunk_size: int = 500) -> List[str]:
        """Split text into chunks while preserving sentence boundaries"""
        sentences = text.replace('\n', ' ').split('. ')
        chunks = []
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Ensure proper sentence ending
            if not sentence.endswith('.'):
                sentence += '.'

            sentence_size = len(sentence)

            # Check if adding this sentence would exceed chunk size
            if current_size + sentence_size > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_size = sentence_size
            else:
                current_chunk.append(sentence)
                current_size += sentence_size

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks
        
    @staticmethod
    def process_document(file_path: str, chunk_size: int = 500) -> Tuple[List[str], List[str], List[Dict]]:
        """Process a single document and prepare it for ChromaDB"""
        try:
            # Read the document
            content = DocumentLoader.read_document(file_path)

            # Split into chunks
            chunks = TextProcessor.split_text(content)

            # Prepare metadata
            file_name = os.path.basename(file_path)
            metadatas = [{"source": file_name, "chunk": i} for i in range(len(chunks))]
            ids = [f"{file_name}_chunk_{i}" for i in range(len(chunks))]

            return ids, chunks, metadatas
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return [], [], []
        
    @staticmethod
    def process_multiple_documents(folder_path: str, chunk_size: int = 500) -> Tuple[List[str], List[str], List[Dict]]:
        """Process all documents in a folder"""
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        all_ids, all_texts, all_metadatas = [], [], []
        supported_extensions = DocumentLoader.get_supported_extensions()
        
        files = [
            os.path.join(folder_path, file) 
            for file in os.listdir(folder_path) 
            if os.path.isfile(os.path.join(folder_path, file)) and 
               any(file.lower().endswith(ext) for ext in supported_extensions)
        ]
        
        for file_path in files:
            print(f"Processing {os.path.basename(file_path)}...")
            ids, texts, metadatas = TextProcessor.process_document(file_path, chunk_size)
            all_ids.extend(ids)
            all_texts.extend(texts)
            all_metadatas.extend(metadatas)
            print(f"Added {len(texts)} chunks from {os.path.basename(file_path)}")
        
        return all_ids, all_texts, all_metadatas
