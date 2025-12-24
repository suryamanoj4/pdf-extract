import sys
import argparse
from pipeline import PDFTextExtractionPipeline, process_single_pdf, analyze_pdf_content


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDFs with Telugu Unicode processing")
    parser.add_argument("pdf_path", help="Path to the PDF file to process")
    parser.add_argument("--format", choices=["dict", "text", "detailed"], default="detailed",
                        help="Output format (default: detailed)")
    parser.add_argument("--analyze", action="store_true",
                        help="Analyze PDF content without full processing")

    args = parser.parse_args()

    if not args.analyze:
        try:
            result = process_single_pdf(args.pdf_path, output_format=args.format)
            print(result)
        except Exception as e:
            print(f"Error processing PDF: {str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            analysis = analyze_pdf_content(args.pdf_path)
            print(analysis)
        except Exception as e:
            print(f"Error analyzing PDF: {str(e)}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
