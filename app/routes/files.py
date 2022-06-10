import os
from flask import Blueprint, redirect, render_template, request
from flask import send_from_directory, url_for, current_app
from werkzeug.utils import secure_filename
from app.models import UploadFile
from app.extensions import db
from app.app_utils import read_workbook

files_bp = Blueprint('files_bp', __name__, template_folder='../templates/files', url_prefix='/files')


ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx'}

def allowed_file(fname:str) -> bool:
    '''returns True if path is valid and file extension is one of allowed'''
    return '.' in fname and fname.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

@files_bp.route('/')
def get_files():
    up_fs = db.session.query(UploadFile).all()
    return render_template('files.html', up_fs=up_fs)

@files_bp.route('/upload', methods=['GET'])
def upload_file():
    accepted_exts = ', '.join(ALLOWED_EXTENSIONS)
    return render_template('upload_file.html', accepted_exts=accepted_exts)

@files_bp.route('/download_file/<int:id>')
def download_file(id:int):
    f_for_download = UploadFile.query.get_or_404(id)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], f_for_download.filename,
        download_name=f_for_download.filename, as_attachment=True)

@files_bp.route('/processing', methods=['POST'])
def processing():
    '''only POST requests are allowed'''
    files = request.files.getlist('file')
    xlsx_values = []
    files_uploaded_counter = 0
    did_some_work = False
    for i, file in enumerate(files, start=1):
        print(f'\n---Iterating files--- f: {file}, filename attr: {file.filename}\n')
        if file.filename == '':
            print('\nNo file selected!\n')
            if i == len(files) and not did_some_work:
                return '<h1>submited without selected files. Handled on wtf-form validators in real cases</h1>'
            else:
                continue
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)            
            save_to_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
            # save_to_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(save_to_path)

            # additionally collect data from  xlsx files
            if save_to_path.lower().endswith('.xlsx'):
                val_from_wb = read_workbook(save_to_path, 5)
                xlsx_values.append(val_from_wb)

            upload_file = UploadFile(filename=filename, fpath=save_to_path, user_upload=False)
            db.session.add(upload_file)
            files_uploaded_counter += 1
            did_some_work = True
    db.session.commit()
    msg = f'Successfully uploaded {files_uploaded_counter} files'
    return render_template('upload_processing.html', msg=msg, xlsx_values=xlsx_values)