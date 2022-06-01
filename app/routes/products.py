from flask import Blueprint, url_for, render_template, request, jsonify, redirect
from app.models import db, Products


prod_bp = Blueprint('prod_bp', __name__, template_folder='../templates/products')


@prod_bp.route('/products', methods=['GET', 'POST'])
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

@prod_bp.route('/products/add_new')
def add_new():
    return render_template('add_product.html')

@prod_bp.route('/products/<int:id>')
def product(id:int):
    prod = db.session.query(Products).filter(Products.id==id).first()
    return jsonify(prod.as_dict())

@prod_bp.route('/products/delete/<int:id>')
def delete(id:int):
    item_to_delete = db.session.query(Products).filter(Products.id==id).delete()
    db.session.commit()
    return redirect(url_for('prod_bp.products'))