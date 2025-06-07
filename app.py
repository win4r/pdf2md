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
        return render_template('result.html', markdown_content=markdown_content, filename=filename)
    else:
        # Invalid file type
        return "Invalid file type. Please upload a PDF."

def process_pdf_to_markdown(pdf_filepath):
    try:
        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory(prefix="pdf2md_webapp_") as temp_dir:
            # Step 1: Convert PDF to images
            # Assuming default DPI and format for now, can be made configurable later
            pdf_processor = PDFProcessor(dpi=300, image_format='png')
            image_paths = pdf_processor.convert_pdf_to_images(pdf_filepath, temp_dir)
            if not image_paths:
                return "Error: Could not convert PDF to images."

            # Step 2: Process images with OCR
            # API key should be configured via .env file (OCRProcessor handles this)
            ocr_processor = OCRProcessor()
            ocr_results = ocr_processor.process_images(image_paths)
            if not ocr_results:
                return "Error: OCR processing failed."

            # Step 3: Generate Markdown
            markdown_generator = MarkdownGenerator()
            markdown_text = markdown_generator.generate_markdown(ocr_results)

            return markdown_text
    except Exception as e:
        # Log the exception e for debugging
        print(f"Error during PDF processing: {e}")
        return f"An error occurred during processing: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
