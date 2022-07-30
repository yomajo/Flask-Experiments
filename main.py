from random import randint
from app.extensions import db
from app.models import User, Products, Brand, UploadFile
from app import create_app


app = create_app()

@app.cli.command()
def createdb():
    db.create_all()

@app.cli.command()
def filldb():
    with open('names.txt', newline='') as f:
        for name in f.readlines():
            new_product = Products(name=name.strip(), qty=randint(1,50))
            db.session.add(new_product)
    db.session.commit()
    print('Added')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Products': Products, 'Brand': Brand, 'UploadFile': UploadFile}