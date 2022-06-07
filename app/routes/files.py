from fileinput import filename
from flask import Blueprint, redirect, render_template, request, send_file, send_from_directory, url_for, current_app
from flask_login import current_user

import os

files_bp = Blueprint('files_bp', __name__, template_folder='../templates/files', url_prefix='/files')


HARDCODED_FNAMES = ['me_so_static.html'] 


@files_bp.route('/')
def get_files():
    return render_template('files.html', fnames=HARDCODED_FNAMES)

@files_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.form['fname']
        print()
        print(uploaded_file)
        print(f'\nNot yet implemented to accept incoming files uploaded with form in route /files/upload\n')
        return redirect(url_for('files_bp.get_files'))
    # GET
    return render_template('upload_file.html')

@files_bp.route('/download_sample')
def download_sample():
    return redirect(url_for('static', filename='/uploaded/sample.JPG'))