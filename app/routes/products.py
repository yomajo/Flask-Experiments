from flask import Blueprint, url_for, render_template, request, jsonify, redirect
from app.models import db, Products, Brand


prod_bp = Blueprint('prod_bp', __name__, template_folder='../templates/products', url_prefix='/products')

HARDCODED_BRANDS = ['BRAND A', 'BRAND B', 'BRAND C', 'BRAND D']

@prod_bp.route('/', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        items = db.session.query(Products).all()
        return render_template('products.html', products=items)

    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        qty = request.form['qty']
        brand = request.form['selected-brand']
        brand_entry = db.session.query(Brand).filter_by(name=brand).first()
        brand_id = brand_entry.id
        
        new_item = Products(id=id, name=name, qty=qty, brand_id=brand_id) if id else Products(name=name, qty=qty, brand_id=brand_id)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('prod_bp.products'))

@prod_bp.route('/add_product')
def add_product():
    brands = [brand.name for brand in  Brand.query.all()]    
    return render_template('add_product.html', brands=brands)

@prod_bp.route('/<int:id>')
def product(id:int):
    prod = db.session.query(Products).filter(Products.id==id).first()
    return jsonify(prod.as_dict())

@prod_bp.route('/delete/<int:id>')
def delete(id:int):
    db.session.query(Products).filter(Products.id==id).delete()
    db.session.commit()
    return redirect(url_for('prod_bp.products'))

@prod_bp.route('/brands')
def brands():
    brands = [brand.name for brand in  Brand.query.all()]
    return f'<h1>{brands}</h1>'
