"""
Test module for the PDF text extraction pipeline with Telugu Unicode processing.
"""
import os
import tempfile
import fitz  # PyMuPDF
from pipeline import PDFTextExtractionPipeline, process_single_pdf, analyze_pdf_content
from pdf_classifier import is_text_based_pdf
from text_extractor import extract_text_from_pdf
from telugu_processor import detect_telugu_unicode, convert_telugu_unicode_to_readable


def create_test_pdf_with_text(content: str, filename: str):
    """Create a test PDF with the given content."""
    doc = fitz.open()
    page = doc.new_page()
    
    # Insert text into the page
    page.insert_text((50, 72), content, fontsize=12)
    
    doc.save(filename)
    doc.close()


def create_sample_telugu_pdf():
    """Create a sample PDF with Telugu text for testing."""
    # Create a temporary PDF file with Telugu text
    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_pdf.close()
    
    # Create a PDF with some Telugu text
    # Using Unicode for Telugu characters
    telugu_text = "హలో ప్రపంచం! ఇది తెలుగు పాఠ్యం. పిడిఎఫ్ నుండి పాఠ్యాన్ని ఉపయోగించడం ఎలా?"
    
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), telugu_text, fontsize=12)
    page.insert_text((50, 100), "This is English text in the same PDF.", fontsize=12)
    doc.save(temp_pdf.name)
    doc.close()
    
    return temp_pdf.name


def create_sample_english_pdf():
    """Create a sample PDF with English text for testing."""
    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    temp_pdf.close()
    
    english_text = "Hello World! This is English text in a PDF. How to extract text from PDFs?"
    
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), english_text, fontsize=12)
    doc.save(temp_pdf.name)
    doc.close()
    
    return temp_pdf.name


def test_pdf_classification():
    """Test PDF classification functionality."""
    print("Testing PDF classification...")
    
    # Create test PDFs
    telugu_pdf_path = create_sample_telugu_pdf()
    english_pdf_path = create_sample_english_pdf()
    
    try:
        # Test Telugu PDF classification
        is_text_based, metadata = is_text_based_pdf(telugu_pdf_path)
        print(f"Telugu PDF is text-based: {is_text_based}")
        print(f"Telugu PDF metadata: {metadata}")
        
        # Test English PDF classification
        is_text_based, metadata = is_text_based_pdf(english_pdf_path)
        print(f"English PDF is text-based: {is_text_based}")
        print(f"English PDF metadata: {metadata}")
        
        print("PDF classification test completed successfully.\n")
        
    finally:
        # Clean up
        os.unlink(telugu_pdf_path)
        os.unlink(english_pdf_path)


def test_text_extraction():
    """Test text extraction functionality."""
    print("Testing text extraction...")
    
    # Create test PDF
    telugu_pdf_path = create_sample_telugu_pdf()
    
    try:
        # Test text extraction
        extraction_result = extract_text_from_pdf(telugu_pdf_path)
        print(f"Extracted text: {extraction_result['full_text']}")
        print(f"Number of pages: {extraction_result['total_pages']}")
        
        print("Text extraction test completed successfully.\n")
        
    finally:
        # Clean up
        os.unlink(telugu_pdf_path)


def test_telugu_processing():
    """Test Telugu Unicode processing."""
    print("Testing Telugu processing...")
    
    # Test text with Telugu characters
    telugu_text = "హలో ప్రపంచం! ఇది తెలుగు పాఠ్యం."
    english_text = "Hello World! This is English text."
    
    # Test detection
    detection_result = detect_telugu_unicode(telugu_text)
    print(f"Telugu detection result: {detection_result}")
    
    # Test conversion
    conversion_result = convert_telugu_unicode_to_readable(telugu_text)
    print(f"Telugu conversion result: {conversion_result}")
    
    # Test with English text (should not have Telugu)
    detection_result_eng = detect_telugu_unicode(english_text)
    print(f"English detection result: {detection_result_eng}")
    
    print("Telugu processing test completed successfully.\n")


def test_full_pipeline():
    """Test the full pipeline."""
    print("Testing full pipeline...")
    
    # Create test PDF
    telugu_pdf_path = create_sample_telugu_pdf()
    
    try:
        # Test the full pipeline
        pipeline = PDFTextExtractionPipeline()
        result = pipeline.process_pdf(telugu_pdf_path, output_format="detailed")
        
        print(f"Pipeline result: {result}")
        
        # Test with different output formats
        result_text = pipeline.process_pdf(telugu_pdf_path, output_format="text")
        print(f"Pipeline result (text format): {result_text}")
        
        result_dict = pipeline.process_pdf(telugu_pdf_path, output_format="dict")
        print(f"Pipeline result (dict format): {result_dict}")
        
        print("Full pipeline test completed successfully.\n")
        
    finally:
        # Clean up
        os.unlink(telugu_pdf_path)


def test_pdf_analysis():
    """Test PDF analysis functionality."""
    print("Testing PDF analysis...")
    
    # Create test PDF
    telugu_pdf_path = create_sample_telugu_pdf()
    
    try:
        # Test PDF analysis
        analysis = analyze_pdf_content(telugu_pdf_path)
        print(f"PDF analysis result: {analysis}")
        
        print("PDF analysis test completed successfully.\n")
        
    finally:
        # Clean up
        os.unlink(telugu_pdf_path)


def run_all_tests():
    """Run all tests."""
    print("Starting tests for PDF text extraction pipeline...\n")
    
    test_pdf_classification()
    test_text_extraction()
    test_telugu_processing()
    test_full_pipeline()
    test_pdf_analysis()
    
    print("All tests completed successfully!")


if __name__ == "__main__":
    run_all_tests()