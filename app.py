import os
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pdf2md.pdf_processor import PDFProcessor
from pdf2md.ocr_processor import OCRProcessor
from pdf2md.markdown_generator import MarkdownGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        # No file part
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        # No selected file
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        markdown_content = process_pdf_to_markdown(filepath)
        # Clean up the uploaded file after processing
        # os.remove(filepath) # Consider if you want to keep or remove the uploaded PDF

        # Check if process_pdf_to_markdown returned an error message (string)
        if isinstance(markdown_content, str) and markdown_content.startswith("Error:"):
            # An error occurred during processing, render index with error
            try:
                if os.path.exists(filepath): # Check if file exists before removing
                    os.remove(filepath)
                    app.logger.info(f"Removed failed upload: {filepath}")
            except OSError as e:
                app.logger.error(f"Error removing failed upload {filepath}: {e}")
            return render_template('index.html', error_message=markdown_content)

        # If successful, consider removing the uploaded PDF if it's no longer needed
        # For now, we keep it as per current commented out os.remove
        # try:
        #     if os.path.exists(filepath):
        #         os.remove(filepath)
        #         app.logger.info(f"Removed successfully processed upload: {filepath}")
        # except OSError as e:
        #     app.logger.error(f"Error removing successfully processed upload {filepath}: {e}")

        return render_template('result.html', markdown_content=markdown_content, filename=filename)
    else:
        # Invalid file type
        return render_template('index.html', error_message="Invalid file type. Please upload a PDF.")

def process_pdf_to_markdown(pdf_filepath):
    """
    Processes the PDF to Markdown.
    Returns the Markdown string on success, or an error message string starting with "Error:" on failure.
    """
    try:
        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory(prefix="pdf2md_webapp_") as temp_dir:
            # Step 1: Convert PDF to images
            pdf_processor = PDFProcessor(dpi=300, image_format='png')
            image_paths = pdf_processor.convert_pdf_to_images(Path(pdf_filepath), Path(temp_dir)) # Ensure Path objects
            if not image_paths:
                return "Error: Could not convert PDF to images. The PDF might be empty, corrupted, or password-protected."

            # Step 2: Process images with OCR
            ocr_processor = OCRProcessor() # Assumes API key is handled by OCRProcessor (e.g., via .env)
            ocr_results = ocr_processor.process_images(image_paths)
            if not ocr_results: # Assuming process_images returns a list, and empty means failure or no text
                # Check if any image was processed but no text found
                if any(isinstance(res, dict) and res.get("text") == "" for res in ocr_results if res): # More specific check if possible
                     return "Error: OCR processing did not find any text in the images. The PDF might be image-based with no textual content."
                return "Error: OCR processing failed. This could be due to API issues or unreadable images."

            # Filter out potential None results if process_images can return them
            valid_ocr_results = [res for res in ocr_results if res and "text" in res]
            if not valid_ocr_results and image_paths: # If there were images but no valid OCR results
                 return "Error: OCR processing yielded no valid text results from the document images."


            # Step 3: Generate Markdown
            markdown_generator = MarkdownGenerator()
            markdown_text = markdown_generator.generate_markdown(valid_ocr_results)
            if not markdown_text.strip(): # If markdown is empty (e.g. only whitespace)
                return "Error: Generated Markdown is empty. This might happen if the PDF contained no recognizable text."

            return markdown_text
    except Exception as e:
        # Log the exception e for debugging
        app.logger.error(f"Error during PDF processing for {pdf_filepath}: {e}", exc_info=True)
        # Provide a more generic error message to the user for security/simplicity
        return f"Error: An unexpected error occurred during processing. Please check the logs for details. ({type(e).__name__})"

if __name__ == '__main__':
    # It's good practice to use app.logger for logging in Flask
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        # Example: Log to a file
        file_handler = RotatingFileHandler('app_errors.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.ERROR)

    app.run(debug=True) # debug=True provides good error pages during development
