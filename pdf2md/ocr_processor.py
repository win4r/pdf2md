"""
Module for OCR processing using Gemini 2.5 Flash API.
"""

import base64
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Union

import google.generativeai as genai
from dotenv import load_dotenv
from tqdm import tqdm


class OCRProcessor:
    """
    Class for OCR processing using Gemini 2.5 Flash API.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OCR processor.

        Args:
            api_key: Gemini API key (optional, will use environment variable if not provided)
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not provided. Please set the GEMINI_API_KEY environment variable "
                "or provide it as a parameter."
            )
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize the Gemini model (using specified model for OCR)
        # 使用用户指定的 gemini-2.5-flash-preview-04-17 模型
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    
    def _encode_image(self, image_path: str) -> str:
        """
        Encode an image file to base64.

        Args:
            image_path: Path to the image file

        Returns:
            Base64-encoded image data
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    def process_image(self, image_path: str, max_retries: int = 3, retry_delay: int = 2) -> str:
        """
        Process a single image with OCR.

        Args:
            image_path: Path to the image file
            max_retries: Maximum number of retries on failure
            retry_delay: Delay between retries in seconds

        Returns:
            Extracted text from the image
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Prepare the prompt for OCR
        prompt = """
        Please perform OCR on this image and extract all the text content. 
        Return ONLY the extracted text, preserving the original formatting as much as possible.
        Do not add any explanations, headers, or additional content.
        """
        
        # Retry logic for API calls
        for attempt in range(max_retries):
            try:
                # Create the image part for the API request
                image_data = {"mime_type": "image/png", "data": self._encode_image(image_path)}
                
                # Generate content using the Gemini API
                response = self.model.generate_content([prompt, image_data])
                
                # Extract and return the text
                return response.text
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Error processing image {image_path}: {e}")
                    print(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    raise RuntimeError(f"Failed to process image after {max_retries} attempts: {e}")
    
    def process_images(self, image_paths: List[str]) -> List[str]:
        """
        Process multiple images with OCR.

        Args:
            image_paths: List of paths to image files

        Returns:
            List of extracted text from each image
        """
        results = []
        
        for image_path in tqdm(image_paths, desc="Processing images with OCR"):
            text = self.process_image(image_path)
            results.append(text)
        
        return results
