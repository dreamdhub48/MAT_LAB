import os
import subprocess
import magic
import PyPDF2

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        static_analysis_result = perform_static_analysis(file_path)
        dynamic_analysis_result = perform_dynamic_analysis(file_path)

        result_text = f"Static Analysis Result: {static_analysis_result}\n\nDynamic Analysis Result: {dynamic_analysis_result}"

        result_file_path = os.path.join(app.config['RESULT_FOLDER'], f"{file.filename.split('.')[0]}_result.txt")
        
        with open(result_file_path, 'w') as result_file:
            result_file.write(result_text)

        return render_template('result.html', filename=file.filename, result=result_text)

def perform_static_analysis(file_path):
    mime = magic.Magic()
    file_type = mime.from_file(file_path)
    if file_type.startswith('application/pdf'):
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            num_pages = pdf_reader.numPages
            return f"PDF document with {num_pages} pages."
    else:
        return f"File type: {file_type}"


def perform_dynamic_analysis(file_path):
    try:
        # Execute the PDF file using a PDF viewer command (e.g., evince)
        subprocess.check_output(['python', file_path], stderr=subprocess.STDOUT, timeout=30)
        return 'No malicious behavior detected during dynamic analysis.'
    except subprocess.CalledProcessError as e:
        return f'Malicious behavior detected: {e.output.decode()}'
    except subprocess.TimeoutExpired:
        return 'Dynamic analysis timed out.'

if __name__ == '__main__':
    app.run(debug=True)
