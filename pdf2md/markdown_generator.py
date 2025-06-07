"""
Module for converting OCR text to Markdown format.
"""

import re
from typing import List, Optional


class MarkdownGenerator:
    """
    Class for converting OCR text to Markdown format.
    """

    def __init__(self):
        """
        Initialize the Markdown generator.
        """
        pass

    def _detect_headings(self, text: str) -> str:
        """
        Detect and format headings in the text.

        Args:
            text: Input text

        Returns:
            Text with Markdown headings
        """
        # Pattern for potential headings (short lines with no punctuation at the end)
        heading_pattern = r"^([A-Z0-9][A-Za-z0-9\s\-:]{0,60})$"
        
        lines = text.split("\n")
        result_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                result_lines.append("")
                continue
                
            # Check if the line looks like a heading
            match = re.match(heading_pattern, line)
            if match and len(line) < 100:  # Limit heading length
                # Determine heading level based on context
                if i == 0 or all(not l.strip() for l in lines[max(0, i-2):i]):
                    # First line or preceded by blank lines - likely a main heading
                    result_lines.append(f"# {line}")
                elif i > 0 and lines[i-1].strip() == "":
                    # Preceded by one blank line - likely a subheading
                    result_lines.append(f"## {line}")
                else:
                    # Just add the line as is
                    result_lines.append(line)
            else:
                result_lines.append(line)
                
        return "\n".join(result_lines)

    def _detect_lists(self, text: str) -> str:
        """
        Detect and format lists in the text.

        Args:
            text: Input text

        Returns:
            Text with Markdown lists
        """
        # Pattern for potential list items
        bullet_patterns = [
            r"^[\s]*[•●○◦*-][\s]+(.+)$",  # Bullet points
            r"^[\s]*(\d+)\.[\s]+(.+)$",    # Numbered lists
        ]
        
        lines = text.split("\n")
        result_lines = []
        
        for line in lines:
            line_processed = False
            
            # Check for bullet lists
            match = re.match(bullet_patterns[0], line)
            if match:
                result_lines.append(f"* {match.group(1)}")
                line_processed = True
                
            # Check for numbered lists
            if not line_processed:
                match = re.match(bullet_patterns[1], line)
                if match:
                    result_lines.append(f"{match.group(1)}. {match.group(2)}")
                    line_processed = True
            
            # If not a list item, add as is
            if not line_processed:
                result_lines.append(line)
                
        return "\n".join(result_lines)

    def _detect_emphasis(self, text: str) -> str:
        """
        Detect and format emphasis (bold, italic) in the text.
        This is a simple heuristic and may not catch all cases.

        Args:
            text: Input text

        Returns:
            Text with Markdown emphasis
        """
        # This is a simplified approach - in a real implementation,
        # more sophisticated NLP might be needed for accurate detection
        return text

    def _format_paragraphs(self, text: str) -> str:
        """
        Format paragraphs in the text.

        Args:
            text: Input text

        Returns:
            Text with properly formatted paragraphs
        """
        # Split text into paragraphs (double newlines)
        paragraphs = re.split(r"\n\s*\n", text)
        
        # Remove extra whitespace within paragraphs
        paragraphs = [re.sub(r"\s+", " ", p.strip()) for p in paragraphs]
        
        # Join paragraphs with double newlines
        return "\n\n".join(paragraphs)

    def generate_markdown(self, ocr_texts: List[str]) -> str:
        """
        Generate Markdown from OCR texts.

        Args:
            ocr_texts: List of OCR text results (one per page)

        Returns:
            Markdown formatted text
        """
        markdown_pages = []
        
        for i, text in enumerate(ocr_texts):
            # Process the text
            processed_text = text
            
            # Format paragraphs
            processed_text = self._format_paragraphs(processed_text)
            
            # Detect and format headings
            processed_text = self._detect_headings(processed_text)
            
            # Detect and format lists
            processed_text = self._detect_lists(processed_text)
            
            # Add page separator if not the last page
            if i < len(ocr_texts) - 1:
                processed_text += "\n\n---\n\n"
                
            markdown_pages.append(processed_text)
        
        # Combine all pages
        return "".join(markdown_pages)
