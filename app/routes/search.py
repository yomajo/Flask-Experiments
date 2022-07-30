from crypt import methods
from flask import Blueprint, url_for, render_template, request, jsonify, redirect
from app.models import db, Products, Brand


search_bp = Blueprint('search_bp', __name__, template_folder='../templates/search', url_prefix='/search')

@search_bp.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        q = request.form.get('search', None)
        if not q:
            return 'No query provided'
        results = db.session.query(Products).search(q)
        return results
    return render_template('search.html')


# @search_bp.route('/results')
# def results(query):
#     if request.method == 'POST':
#     return results
