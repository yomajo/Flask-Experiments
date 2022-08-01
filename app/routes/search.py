from flask import Blueprint, url_for, render_template, request, jsonify, redirect
from app.models import db, Products, Brand
from app.extensions import search

search_bp = Blueprint('search_bp', __name__, template_folder='../templates/search', url_prefix='/search')


@search_bp.route('/', methods=['GET', 'POST'])
def search():
    # available at localhost/search
    if request.method == 'POST':
        q = request.form.get('q', None)
        print(f'\nquery: {q}\n')
        
        results_raw = Products.query.msearch(q, fields=['name'], limit=10)
        print(results_raw)

        results = results_raw.all()
        print(results)

        return render_template('results.html', results=results, query=q)
        
    return render_template('search.html')