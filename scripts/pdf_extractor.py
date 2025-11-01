"""
PDF text extraction module
"""

import pdfplumber
from typing import Dict, Any

class PDFExtractor:
    """Extract text from PDF files"""
    
    def extract_all(self, pdf_path: str, max_pages: int = None) -> Dict[str, Any]:
        """
        Extract text from PDF
        
        Args:
            pdf_path: Path to PDF file
            max_pages: Optional limit on pages to process
            
        Returns:
            Dictionary with text, pages_processed, total_pages, tables_found
        """
        result = {
            'text': '',
            'pages_processed': 0,
            'total_pages': 0,
            'tables_found': 0
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                result['total_pages'] = len(pdf.pages)
                
                # Determine pages to process
                pages_to_process = pdf.pages[:max_pages] if max_pages else pdf.pages
                
                for page in pages_to_process:
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        result['text'] += page_text + "\n\n"
                    
                    # Count tables
                    tables = page.extract_tables()
                    if tables:
                        result['tables_found'] += len(tables)
                
                result['pages_processed'] = len(pages_to_process)
        
        except Exception as e:
            result['error'] = str(e)
        
        return result

# For testing
if __name__ == "__main__":
    extractor = PDFExtractor()
    print("✅ PDFExtractor initialized")
