"""
Module for extracting text from text-based PDFs using PyMuPDF.
"""
import fitz  # PyMuPDF
from typing import List, Dict, Optional


def extract_text_from_pdf(pdf_path: str, extract_metadata: bool = True) -> Dict:
    """
    Extract text from a text-based PDF using PyMuPDF.
    
    Args:
        pdf_path: Path to the PDF file
        extract_metadata: Whether to extract metadata along with text
        
    Returns:
        Dictionary containing extracted text and metadata
    """
    try:
        doc = fitz.open(pdf_path)
        pages_text = []
        metadata = {}
        
        # Extract document metadata if requested
        if extract_metadata:
            metadata = {
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "producer": doc.metadata.get("producer", ""),
                "creation_date": doc.metadata.get("creationDate", ""),
                "modification_date": doc.metadata.get("modDate", ""),
                "format": doc.metadata.get("format", ""),
                "encryption": doc.metadata.get("encryption", ""),
            }
        
        # Extract text from each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract text with formatting information
            text = page.get_text("text")  # Simple text extraction
            blocks = page.get_text("dict")  # More detailed extraction with positioning
            
            page_info = {
                "page_number": page_num + 1,
                "text": text,
                "block_count": len(blocks.get("blocks", [])),
                "width": page.rect.width,
                "height": page.rect.height,
            }
            
            pages_text.append(page_info)
        
        doc.close()
        
        result = {
            "pdf_path": pdf_path,
            "total_pages": len(pages_text),
            "pages": pages_text,
            "full_text": "\n".join([page["text"] for page in pages_text]),
            "metadata": metadata
        }
        
        return result
        
    except Exception as e:
        raise Exception(f"Error extracting text from PDF {pdf_path}: {str(e)}")


def extract_text_by_method(pdf_path: str, method: str = "text") -> str:
    """
    Extract text using different methods available in PyMuPDF.
    
    Args:
        pdf_path: Path to the PDF file
        method: Extraction method ("text", "blocks", "dict", "html", "json", "textpage")
        
    Returns:
        Extracted text as string
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            if method == "text":
                text = page.get_text()
            elif method == "blocks":
                blocks = page.get_text("blocks")
                text = "\n".join([block[4] for block in blocks if block[6] == 0])  # Only text blocks
            elif method == "dict":
                page_dict = page.get_text("dict")
                text = ""
                for block in page_dict.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text += span["text"] + " "
                        text += "\n"
            elif method == "html":
                text = page.get_text("html")
            elif method == "json":
                text = page.get_text("json")
            else:
                raise ValueError(f"Unknown extraction method: {method}")
            
            full_text += f"\n--- Page {page_num + 1} ---\n{text}\n"
        
        doc.close()
        return full_text.strip()
        
    except Exception as e:
        raise Exception(f"Error extracting text with method '{method}' from PDF {pdf_path}: {str(e)}")


def extract_text_with_formatting(pdf_path: str) -> List[Dict]:
    """
    Extract text with formatting information (font, size, color, etc.).
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dictionaries containing text with formatting information
    """
    try:
        doc = fitz.open(pdf_path)
        formatted_text = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_dict = page.get_text("dict")
            
            page_formatted = {
                "page_number": page_num + 1,
                "blocks": []
            }
            
            for block in page_dict.get("blocks", []):
                if "lines" in block:  # Text block
                    block_formatted = {
                        "type": "text",
                        "bbox": block[:4],  # bounding box
                        "lines": []
                    }
                    
                    for line in block["lines"]:
                        line_formatted = {
                            "spans": []
                        }
                        
                        for span in line["spans"]:
                            span_formatted = {
                                "text": span["text"],
                                "bbox": span["bbox"],
                                "font": span["font"],
                                "size": span["size"],
                                "flags": span["flags"],
                                "color": span["color"],
                                "text_color": "#{:06x}".format(span["color"]) if span["color"] >= 0 else "#000000",
                                "ascender": span["ascender"],
                                "descender": span["descender"]
                            }
                            line_formatted["spans"].append(span_formatted)
                        
                        block_formatted["lines"].append(line_formatted)
                    
                    page_formatted["blocks"].append(block_formatted)
                else:  # Image block
                    block_formatted = {
                        "type": "image",
                        "bbox": block[:4]
                    }
                    page_formatted["blocks"].append(block_formatted)
            
            formatted_text.append(page_formatted)
        
        doc.close()
        return formatted_text
        
    except Exception as e:
        raise Exception(f"Error extracting formatted text from PDF {pdf_path}: {str(e)}")