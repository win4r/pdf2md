"""
Command-line interface for the PDF to Markdown converter.
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

from pdf2md.pdf_processor import PDFProcessor
from pdf2md.ocr_processor import OCRProcessor
from pdf2md.markdown_generator import MarkdownGenerator


def main():
    """
    Main entry point for the CLI.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown using Gemini 2.5 Flash API for OCR"
    )
    parser.add_argument(
        "--input", "-i", required=True, help="Path to the input PDF file"
    )
    parser.add_argument(
        "--output", "-o", help="Path to the output Markdown file (default: input filename with .md extension)"
    )
    parser.add_argument(
        "--dpi", type=int, default=300, help="DPI for image conversion (default: 300)"
    )
    parser.add_argument(
        "--format", choices=["png", "jpg"], default="png", help="Image format for conversion (default: png)"
    )
    parser.add_argument(
        "--api-key", help="Gemini API key (optional, will use GEMINI_API_KEY environment variable if not provided)"
    )
    parser.add_argument(
        "--temp-dir", help="Directory to store temporary files (optional, default: system temp directory)"
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # Set output file if not provided
    if not args.output:
        input_path = Path(args.input)
        args.output = str(input_path.with_suffix(".md"))

    # Create temporary directory if not provided
    temp_dir = args.temp_dir
    if not temp_dir:
        temp_dir = tempfile.mkdtemp(prefix="pdf2md_")
    else:
        os.makedirs(temp_dir, exist_ok=True)

    try:
        print(f"Processing PDF: {args.input}")
        print(f"Output will be saved to: {args.output}")

        # Step 1: Convert PDF to images
        print("\nStep 1: Converting PDF to images...")
        pdf_processor = PDFProcessor(dpi=args.dpi, image_format=args.format)
        image_paths = pdf_processor.convert_pdf_to_images(args.input, temp_dir)
        print(f"Generated {len(image_paths)} images")

        # Step 2: Process images with OCR
        print("\nStep 2: Processing images with OCR...")
        ocr_processor = OCRProcessor(api_key=args.api_key)
        ocr_results = ocr_processor.process_images(image_paths)
        print(f"Processed {len(ocr_results)} images with OCR")

        # Step 3: Generate Markdown
        print("\nStep 3: Generating Markdown...")
        markdown_generator = MarkdownGenerator()
        markdown_text = markdown_generator.generate_markdown(ocr_results)

        # Step 4: Save Markdown to file
        print(f"\nStep 4: Saving Markdown to {args.output}...")
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        print(f"\nSuccess! Markdown file saved to: {args.output}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
