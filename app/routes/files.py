import os
from flask import Blueprint, redirect, render_template, request
from flask import send_from_directory, url_for, current_app
from werkzeug.utils import secure_filename
from app.models import UploadFile
from app.extensions import db

files_bp = Blueprint('files_bp', __name__, template_folder='../templates/files', url_prefix='/files')


ALLOWED_EXTENSIONS = {'csv', 'txt', 'html', 'jpg', 'jpeg'}

def allowed_file(fname:str) -> bool:
    '''returns True if path is valid and file extension is one of allowed'''
    return '.' in fname and fname.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

@files_bp.route('/')
def get_files():
    up_fs = db.session.query(UploadFile).all()
    return render_template('files.html', up_fs=up_fs)

@files_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('\nRequest has no file object inside request.files!\n')
            return redirect(url_for('files_bp.get_files'))
        file = request.files['file']
        print(f'\nThis is file: {file}\nhas filename property: {file.filename}\n')
        if file.filename == '':
            print('\nNo file selected!\n')
            return redirect(url_for('files_bp.get_files'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)            
            save_to_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
            file.save(save_to_path)

            upload_file = UploadFile(filename=filename, fpath=save_to_path, user_upload=False)
            db.session.add(upload_file)
            db.session.commit()
            return redirect(url_for('files_bp.get_files'))
        
    # GET
    accepted_exts = ', '.join(ALLOWED_EXTENSIONS)
    return render_template('upload_file.html', accepted_exts=accepted_exts)

@files_bp.route('/download_file/<int:id>')
def download_file(id:int):
    f_for_download = UploadFile.query.get_or_404(id)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], f_for_download.filename, download_name=f_for_download.filename, as_attachment=True)
