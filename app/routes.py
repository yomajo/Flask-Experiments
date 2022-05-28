from flask import Blueprint, url_for, render_template, request, jsonify, redirect
from app.models import db, Products

bp = Blueprint('bp', __name__)


@bp.route('/')
def index():
    return render_template('index.html')
    

@bp.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        items = db.session.query(Products).all()
        return render_template('products.html', products=items)

    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        qty = request.form['qty']        
        new_item = Products(id=id, name=name, qty=qty) if id else Products(name=name, qty=qty)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('bp.products'))

@bp.route('/product/<int:id>')
def product(id:int):
    prod = db.session.query(Products).filter(Products.id==id).first()
    return jsonify(prod.as_dict())

@bp.route('/add_new')
def add_new():
    return render_template('add_new.html')

@bp.route('/products/delete/<int:id>')
def delete(id:int):
    item_to_delete = db.session.query(Products).filter(Products.id==id).delete()
    db.session.commit()
    return redirect(url_for('bp.products'))

