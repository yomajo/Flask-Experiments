from flask import Blueprint, url_for, render_template, request, jsonify, redirect
from app.models import db, Products, Brand


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
        brand_name = request.form['selected-brand']        
        new_item = Products(id=id, name=name, qty=qty, brand_id=brand_name) if id else Products(name=name, qty=qty, brand_name=brand_name)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('prod_bp.products'))

@prod_bp.route('/add_product')
def add_product():
    brands = [brand.name for brand in  Brand.query.all()]    
    return render_template('add_product.html', brands=brands)

@prod_bp.route('/<int:id>')
def product(id:int):
    prod = db.session.query(Products).get_or_404(id)
    return jsonify(prod.as_dict())

@prod_bp.route('/delete/<int:id>')
def delete(id:int):
    db.session.query(Products).filter(Products.id==id).delete()
    db.session.commit()
    return redirect(url_for('prod_bp.products'))

@prod_bp.route('/brands')
def brands():
    brands = [brand.name for brand in Brand.query.all()]
    return f'<h1>{brands}</h1>'

@prod_bp.route('/explore_brands')
def explore_brands():
    '''learning about queries, db models and foreign keys'''
    brand_entries = db.session.query(Brand).filter_by(name='Utenos').all()
    brand_products = [entry.products for entry in brand_entries]
    return f'<h1>{brand_products}</h1>'
