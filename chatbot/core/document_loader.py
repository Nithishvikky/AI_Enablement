import os
import PyPDF2
import docx
from typing import Optional

class DocumentLoader:
    """Handles loading documents from various file formats"""
    
    # Add this missing class attribute
    SUPPORTED_EXTENSIONS = ['.txt', '.pdf', '.docx']

    @staticmethod
    def read_text_file(file_path: str) -> str:
        """Read content from a text file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    @staticmethod
    def read_pdf_file(file_path: str) -> str:
        """Read content from a PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
        
    @staticmethod
    def read_docx_file(file_path: str) -> str:
        """Read content from a Word document"""
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

        
    @staticmethod
    def read_document(file_path: str) -> str:
        """Read document content based on file extension"""
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension == '.txt':
            return DocumentLoader.read_text_file(file_path)
        elif file_extension == '.pdf':
            return DocumentLoader.read_pdf_file(file_path)
        elif file_extension == '.docx':
            return DocumentLoader.read_docx_file(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    @staticmethod
    def get_supported_extensions() -> list:
        """Return list of supported file extensions"""
        return DocumentLoader.SUPPORTED_EXTENSIONS.copy()
