from app.extensions import db
from app.models import User, Products, Brand, UploadFile, SKU
from app import create_app


app = create_app()

''' __tablename__ = 'sku'
    sku = db.Column(db.String(100), primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    same_weight_lsts = db.Column(db.Boolean, default=True)

    upload_id = db.Column(db.Integer, ForeignKey('uploadfile.id'))
    file = db.relationship('UploadFile')

    __tablename__ = 'uploadfile'
    id = db.Column(db.Integer, primary_key=True)
    fpath = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)'''

@app.cli.command()
def createdb():
    db.create_all()

@app.cli.command()
def dropdb():
    db.drop_all()

@app.cli.command()
def addsome():
    new_sku = SKU(sku='cool_thing', same_weight_lsts=True)
    new_upload = UploadFile(fpath='/home/devyo/bla/bla/yo/coolstuff.txt')

    db.session.add(new_upload)
    db.session.flush()
    new_sku.upload_id = new_upload.id
    
    db.session.add(new_sku)
    db.session.commit()
    print('<cool_thing> sku added with related upload')
    print(f'Resulting SKU obj:\n{new_sku}')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Products': Products, 'Brand': Brand, 'UploadFile': UploadFile, 'SKU': SKU}