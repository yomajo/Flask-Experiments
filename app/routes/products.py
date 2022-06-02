from flask import Blueprint, url_for, render_template, request, jsonify, redirect
from app.models import db, Products


prod_bp = Blueprint('prod_bp', __name__, template_folder='../templates/products', url_prefix='/products')


@prod_bp.route('/', methods=['GET', 'POST'])
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
        return redirect(url_for('prod_bp.products'))

@prod_bp.route('/add_product')
def add_product():
    return render_template('add_product.html')

@prod_bp.route('/<int:id>')
def product(id:int):
    prod = db.session.query(Products).filter(Products.id==id).first()
    return jsonify(prod.as_dict())

@prod_bp.route('/delete/<int:id>')
def delete(id:int):
    item_to_delete = db.session.query(Products).filter(Products.id==id).delete()
    db.session.commit()
    return redirect(url_for('prod_bp.products'))