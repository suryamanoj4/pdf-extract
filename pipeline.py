"""
Main pipeline for PDF text extraction with Telugu Unicode processing.
"""
import os
from typing import Dict, Any, Optional
from pdf_classifier import is_text_based_pdf
from text_extractor import extract_text_from_pdf
from telugu_processor import convert_telugu_unicode_to_readable, detect_telugu_unicode


class PDFTextExtractionPipeline:
    """
    Main pipeline class for extracting text from PDFs with Telugu Unicode processing.
    """
    
    def __init__(self):
        self.classifier = None
        self.extractor = None
        self.telugu_processor = None
    
    def process_pdf(self, pdf_path: str, output_format: str = "dict") -> Dict[str, Any]:
        """
        Process a PDF file through the entire pipeline.
        
        Args:
            pdf_path: Path to the PDF file to process
            output_format: Format for the output ("dict", "text", "detailed")
            
        Returns:
            Processed results in the specified format
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        # Step 1: Classify the PDF as text-based or image-based
        is_text_based, classification_metadata = is_text_based_pdf(pdf_path)
        
        result = {
            "pdf_path": pdf_path,
            "is_text_based": is_text_based,
            "classification_metadata": classification_metadata,
            "processing_steps": {
                "classification": True,
                "extraction": False,
                "telugu_processing": False
            }
        }
        
        if not is_text_based:
            result["status"] = "image_based_pdf"
            result["message"] = "PDF is image-based, text extraction not possible"
            return self._format_output(result, output_format)
        
        # Step 2: Extract text from the PDF
        try:
            extraction_result = extract_text_from_pdf(pdf_path)
            result["extraction_result"] = extraction_result
            result["processing_steps"]["extraction"] = True
            
            # Step 3: Process for Telugu Unicode
            full_text = extraction_result["full_text"]
            telugu_processing_result = convert_telugu_unicode_to_readable(full_text)
            
            result["telugu_processing_result"] = telugu_processing_result
            result["processing_steps"]["telugu_processing"] = True
            result["status"] = "success"
            result["message"] = "PDF processed successfully"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            result["message"] = f"Error during text extraction or processing: {str(e)}"
        
        return self._format_output(result, output_format)
    
    def _format_output(self, result: Dict, output_format: str) -> Any:
        """
        Format the output based on the requested format.
        
        Args:
            result: Raw result dictionary
            output_format: Desired output format
            
        Returns:
            Formatted result
        """
        if output_format == "text":
            # Return just the processed text if available
            if "telugu_processing_result" in result:
                return result["telugu_processing_result"]["processed_text"]
            elif "extraction_result" in result:
                return result["extraction_result"]["full_text"]
            else:
                return ""
        
        elif output_format == "detailed":
            # Return the full detailed result
            return result
        
        else:  # Default to dict format
            # Return a concise result dictionary
            concise_result = {
                "pdf_path": result["pdf_path"],
                "is_text_based": result["is_text_based"],
                "status": result["status"],
                "message": result.get("message", ""),
            }
            
            if result["status"] == "success":
                if "telugu_processing_result" in result:
                    concise_result["has_telugu"] = result["telugu_processing_result"]["is_telugu_present"]
                    concise_result["processed_text"] = result["telugu_processing_result"]["processed_text"][:500] + "..." \
                        if len(result["telugu_processing_result"]["processed_text"]) > 500 \
                        else result["telugu_processing_result"]["processed_text"]
            
            return concise_result


def process_single_pdf(pdf_path: str, output_format: str = "detailed") -> Dict[str, Any]:
    """
    Convenience function to process a single PDF file.
    
    Args:
        pdf_path: Path to the PDF file to process
        output_format: Format for the output ("dict", "text", "detailed")
        
    Returns:
        Processed results in the specified format
    """
    pipeline = PDFTextExtractionPipeline()
    return pipeline.process_pdf(pdf_path, output_format)


def process_multiple_pdfs(pdf_paths: list, output_format: str = "detailed") -> Dict[str, Any]:
    """
    Process multiple PDF files.
    
    Args:
        pdf_paths: List of paths to PDF files to process
        output_format: Format for the output ("dict", "text", "detailed")
        
    Returns:
        Dictionary with results for each PDF
    """
    pipeline = PDFTextExtractionPipeline()
    results = {}
    
    for pdf_path in pdf_paths:
        try:
            results[pdf_path] = pipeline.process_pdf(pdf_path, output_format)
        except Exception as e:
            results[pdf_path] = {
                "pdf_path": pdf_path,
                "status": "error",
                "error": str(e),
                "message": f"Error processing PDF: {str(e)}"
            }
    
    return results


def analyze_pdf_content(pdf_path: str) -> Dict[str, Any]:
    """
    Analyze the content of a PDF file without full processing.
    
    Args:
        pdf_path: Path to the PDF file to analyze
        
    Returns:
        Analysis results
    """
    # Just classify and get basic info without full text extraction
    is_text_based, classification_metadata = is_text_based_pdf(pdf_path)
    
    analysis = {
        "pdf_path": pdf_path,
        "is_text_based": is_text_based,
        "classification_metadata": classification_metadata,
        "content_analysis": {
            "is_suitable_for_text_extraction": is_text_based,
            "estimated_content_pages": classification_metadata.get("pages_with_text", 0),
            "estimated_text_density": classification_metadata.get("avg_chars_per_page", 0)
        }
    }
    
    if is_text_based:
        # Do a quick check for Telugu content without full processing
        try:
            # Extract just a sample of text to check for Telugu
            extraction_result = extract_text_from_pdf(pdf_path)
            sample_text = extraction_result["full_text"][:1000]  # First 1000 chars
            telugu_detection = detect_telugu_unicode(sample_text)
            
            analysis["telugu_analysis"] = {
                "has_telugu": telugu_detection["has_telugu"],
                "telugu_percentage": telugu_detection["telugu_percentage"],
                "telugu_chars_count": telugu_detection["total_telugu_chars"]
            }
        except Exception:
            analysis["telugu_analysis"] = {
                "has_telugu": False,
                "error": "Could not analyze for Telugu content"
            }
    
    return analysis