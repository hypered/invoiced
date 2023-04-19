from flask import Flask, request, redirect, url_for, flash, send_from_directory, render_template, session
import os
import uuid
from werkzeug.utils import secure_filename

from . import core

# Set the path for uploaded files and allowed extensions
UPLOAD_DIR = os.environ.get('UPLOAD_DIR', './uploads/')
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__, template_folder=core.JINJA2_TEMPLATES_DIR)
app.config['UPLOAD_DIR'] = UPLOAD_DIR
app.secret_key = 'super_secret_key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def user_generated_directory():
    user_directory = session.get('user_directory', None)
    if user_directory is None:
        user_directory = str(uuid.uuid4())
        session['user_directory'] = user_directory
    joined_path = os.path.join('generated', user_directory)
    return joined_path

def process_file(pdf_path, out_directory):
    result = core.process_pdf(pdf_path, out_directory)
    content = {
        "image_url": os.path.join('generated/per-session', 'output.png'),
        "qr_code_url": os.path.join('generated/per-session', 'qrcode.png'),
        "iban": result['iban'],
        "amount": result['amount'],
        "reference": result['reference'],
    }

    return render_template('preview.html', **content)

@app.route('/generated/per-session/<path:filename>')
def serve_generated_files(filename):
    user_directory = user_generated_directory()
    abs_user_directory = os.path.abspath(user_directory)
    return send_from_directory(abs_user_directory, filename, cache_timeout=0)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Filename extension is not "pdf"')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_DIR'], filename)
        file.save(pdf_path)
        out_directory = user_generated_directory()
        return process_file(pdf_path, out_directory)

    else:
        return render_template('index.html')

def start_server():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    app.run(debug=True)
