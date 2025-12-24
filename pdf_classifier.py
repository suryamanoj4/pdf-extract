"""
Module for classifying PDFs as text-based or image-based.
"""
import fitz  # PyMuPDF
from typing import Tuple


def is_text_based_pdf(pdf_path: str) -> Tuple[bool, dict]:
    """
    Determine if a PDF is text-based or image-based.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Tuple of (is_text_based: bool, metadata: dict)
    """
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        if total_pages == 0:
            return False, {"pages": 0, "has_text": False, "avg_chars_per_page": 0}
        
        pages_with_text = 0
        total_chars = 0
        page_details = []
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # Extract text from the page
            text = page.get_text()
            char_count = len(text.strip())
            
            # Check if page has significant text content
            if char_count > 10:  # Threshold to avoid considering page numbers/headers as content
                pages_with_text += 1
            
            total_chars += char_count
            page_details.append({
                "page_num": page_num + 1,
                "char_count": char_count,
                "has_text": char_count > 10
            })
        
        doc.close()
        
        avg_chars_per_page = total_chars / total_pages
        majority_pages_have_text = pages_with_text / total_pages > 0.5
        
        is_text_based = majority_pages_have_text and avg_chars_per_page > 50
        
        metadata = {
            "pages": total_pages,
            "pages_with_text": pages_with_text,
            "total_chars": total_chars,
            "avg_chars_per_page": avg_chars_per_page,
            "majority_pages_have_text": majority_pages_have_text,
            "page_details": page_details
        }
        
        return is_text_based, metadata
        
    except Exception as e:
        raise Exception(f"Error processing PDF {pdf_path}: {str(e)}")


def check_pdf_fonts(pdf_path: str) -> dict:
    """
    Check fonts used in the PDF to determine if it contains text elements.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with font information
    """
    try:
        doc = fitz.open(pdf_path)
        font_info = {"fonts_used": set(), "pages_with_fonts": 0}
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Get font information for the page
            textpage = page.get_textpage()
            blocks = textpage.extractBLOCKS()
            
            for block in blocks:
                # Check if the block contains text
                if block[6] == 0:  # Block type 0 is text
                    # Extract font information if available
                    # This is a simplified check - actual font detection would be more complex
                    page_text = page.get_text("dict")
                    for x in page_text.get("blocks", []):
                        if "lines" in x:
                            for line in x["lines"]:
                                for span in line["spans"]:
                                    font_info["fonts_used"].add(span.get("font", "unknown"))
        
        doc.close()
        
        font_info["fonts_used"] = list(font_info["fonts_used"])
        return font_info
        
    except Exception as e:
        raise Exception(f"Error checking fonts in PDF {pdf_path}: {str(e)}")