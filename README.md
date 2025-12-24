# PDF Text Extraction Pipeline with Telugu Unicode Processing

A Python-based pipeline for extracting text from PDFs with special handling for Telugu Unicode characters. This tool can classify PDFs as text-based or image-based, extract text content, and properly process Telugu Unicode to ensure readability.

## Features

- **PDF Classification**: Automatically determines if a PDF is text-based or image-based
- **Text Extraction**: Extracts text from text-based PDFs using PyMuPDF
- **Telugu Unicode Processing**: Detects and normalizes Telugu Unicode characters for proper readability
- **Multiple Output Formats**: Supports dictionary, text-only, and detailed output formats
- **Content Analysis**: Provides PDF content analysis without full processing
- **Metadata Extraction**: Retrieves PDF metadata during text extraction

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pdf-extract
   ```

2. Install dependencies using uv (recommended) or pip:
   ```bash
   # Using uv (as per pyproject.toml)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   # Or directly:
   pip install pymupdf chardet
   ```

## Usage

### Command Line Interface

The tool provides a command-line interface for easy PDF processing:

```bash
# Basic usage - process a PDF and get detailed output
python main.py path/to/your/pdf_file.pdf

# Get text-only output
python main.py path/to/your/pdf_file.pdf --format text

# Get concise dictionary output
python main.py path/to/your/pdf_file.pdf --format dict

# Analyze PDF content without full processing
python main.py path/to/your/pdf_file.pdf --analyze
```

### As a Python Module

You can also use the pipeline directly in your Python code:

```python
from pipeline import process_single_pdf, process_multiple_pdfs, analyze_pdf_content

# Process a single PDF
result = process_single_pdf("path/to/pdf.pdf", output_format="detailed")
print(result)

# Process multiple PDFs
results = process_multiple_pdfs(["pdf1.pdf", "pdf2.pdf"], output_format="dict")
print(results)

# Analyze PDF content
analysis = analyze_pdf_content("path/to/pdf.pdf")
print(analysis)
```

## Project Structure

```
pdf-extract/
├── main.py                 # Command-line interface entry point
├── pipeline.py             # Main processing pipeline
├── pdf_classifier.py       # PDF classification logic
├── text_extractor.py       # Text extraction functionality
├── telugu_processor.py     # Telugu Unicode processing
├── test_pipeline.py        # Tests for the pipeline
├── pyproject.toml          # Project dependencies and metadata
├── README.md              # This file
└── test-*.pdf             # Test PDF files
```

## How It Works

### 1. PDF Classification (`pdf_classifier.py`)
- Uses PyMuPDF to open and analyze the PDF
- Counts characters per page to determine if the PDF is text-based or image-based
- A PDF is considered text-based if more than 50% of pages have significant text content (>10 characters per page with an average of >50 characters per page)

### 2. Text Extraction (`text_extractor.py`)
- Extracts text from text-based PDFs using PyMuPDF
- Provides multiple extraction methods (simple text, blocks, formatted text)
- Retrieves PDF metadata (title, author, creation date, etc.)
- Maintains page-level text organization

### 3. Telugu Unicode Processing (`telugu_processor.py`)
- Detects Telugu Unicode characters (Unicode range U+0C00 to U+0C7F)
- Normalizes Telugu text to handle common Unicode issues
- Validates Telugu Unicode sequences
- Extracts Telugu-specific statistics (word count, character distribution)

### 4. Main Pipeline (`pipeline.py`)
- Orchestrates the entire process
- Handles error management and result formatting
- Supports multiple output formats for different use cases

## Output Formats

- **`detailed`** (default): Complete processing result with all metadata and processing steps
- **`dict`**: Concise dictionary with essential information (path, status, processed text excerpt)
- **`text`**: Raw processed text only, suitable for further processing

## Testing

Run the provided tests to verify functionality:

```bash
python -m pytest test_pipeline.py
```

## Dependencies

- `pymupdf` (>=1.23.0): For PDF processing and text extraction
- `chardet` (>=5.0.0): For character encoding detection

## Supported PDF Types

- **Text-based PDFs**: Fully supported with text extraction and Telugu processing
- **Image-based PDFs**: Detected but not processed (text extraction not possible)
- **Mixed PDFs**: Handled based on the majority of pages with text content

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Specify your license here]

## Acknowledgments

- Uses PyMuPDF for PDF processing capabilities
- Unicode handling based on standard Unicode character ranges for Telugu script