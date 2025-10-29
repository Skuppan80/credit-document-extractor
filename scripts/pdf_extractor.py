"""
PDF Text Extraction Module
Extracts text and tables from credit documents
"""

import pdfplumber
from typing import Dict, List, Any

class PDFExtractor:
    """Extract text and tables from PDF documents"""
    
    def __init__(self):
        self.current_file = None
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract all text from PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        text = ""
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        return text
    
    def extract_tables(self, pdf_path: str) -> List[List[List]]:
        """
        Extract all tables from PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of tables (each table is list of rows)
        """
        tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)
        
        return tables
    
    def extract_all(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract text and tables
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with text and tables
        """
        return {
            'text': self.extract_text(pdf_path),
            'tables': self.extract_tables(pdf_path),
            'file_path': pdf_path
        }

# For testing
if __name__ == "__main__":
    extractor = PDFExtractor()
    print("✅ PDF Extractor module loaded")