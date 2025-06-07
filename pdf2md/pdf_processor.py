"""
Module for converting PDF files to images.
"""

import os
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

import fitz  # PyMuPDF
import pdf2image
from tqdm import tqdm


class PDFProcessor:
    """
    Class for converting PDF files to images.
    """

    def __init__(self, dpi: int = 300, image_format: str = "png"):
        """
        Initialize the PDF processor.

        Args:
            dpi: DPI for image conversion
            image_format: Image format for conversion (png or jpg)
        """
        self.dpi = dpi
        self.image_format = image_format.lower()
        if self.image_format not in ["png", "jpg", "jpeg"]:
            raise ValueError("Image format must be png, jpg, or jpeg")
        
        # Normalize jpg/jpeg
        if self.image_format == "jpg":
            self.image_format = "jpeg"

    def convert_pdf_to_images_pymupdf(self, pdf_path: str, output_dir: Optional[str] = None) -> List[str]:
        """
        Convert PDF to images using PyMuPDF.

        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save the images (optional)

        Returns:
            List of paths to the generated images
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create output directory if not provided
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="pdf2md_")
        else:
            os.makedirs(output_dir, exist_ok=True)

        # Open the PDF
        pdf_document = fitz.open(pdf_path)
        num_pages = len(pdf_document)
        image_paths = []

        # Process each page
        for page_num in tqdm(range(num_pages), desc="Converting PDF to images"):
            page = pdf_document.load_page(page_num)
            
            # Convert page to pixmap
            pix = page.get_pixmap(matrix=fitz.Matrix(self.dpi/72, self.dpi/72))
            
            # Generate output path
            output_path = os.path.join(output_dir, f"page_{page_num + 1}.{self.image_format}")
            
            # Save the image
            if self.image_format == "png":
                pix.save(output_path)
            else:  # jpeg
                pix.save(output_path, "jpeg")
                
            image_paths.append(output_path)
            
        pdf_document.close()
        return image_paths

    def convert_pdf_to_images_pdf2image(self, pdf_path: str, output_dir: Optional[str] = None) -> List[str]:
        """
        Convert PDF to images using pdf2image.

        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save the images (optional)

        Returns:
            List of paths to the generated images
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create output directory if not provided
        if output_dir is None:
            output_dir = tempfile.mkdtemp(prefix="pdf2md_")
        else:
            os.makedirs(output_dir, exist_ok=True)

        # Convert PDF to images
        images = pdf2image.convert_from_path(
            pdf_path,
            dpi=self.dpi,
            fmt=self.image_format,
            output_folder=output_dir,
            output_file=f"page_",
            paths_only=True,
        )
        
        return images

    def convert_pdf_to_images(self, pdf_path: str, output_dir: Optional[str] = None, 
                              use_pymupdf: bool = True) -> List[str]:
        """
        Convert PDF to images using the preferred method.

        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save the images (optional)
            use_pymupdf: Whether to use PyMuPDF (True) or pdf2image (False)

        Returns:
            List of paths to the generated images
        """
        try:
            if use_pymupdf:
                return self.convert_pdf_to_images_pymupdf(pdf_path, output_dir)
            else:
                return self.convert_pdf_to_images_pdf2image(pdf_path, output_dir)
        except Exception as e:
            # If one method fails, try the other
            print(f"Error using {'PyMuPDF' if use_pymupdf else 'pdf2image'}: {e}")
            print(f"Trying {'pdf2image' if use_pymupdf else 'PyMuPDF'} instead...")
            
            try:
                if use_pymupdf:
                    return self.convert_pdf_to_images_pdf2image(pdf_path, output_dir)
                else:
                    return self.convert_pdf_to_images_pymupdf(pdf_path, output_dir)
            except Exception as e2:
                raise RuntimeError(f"Failed to convert PDF to images: {e2}")
