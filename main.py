from app.extensions import db
from app.models import User, Products, Brand, UploadFile
from app import create_app


app = create_app()

@app.cli.command()
def createdb():
    db.create_all()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Products': Products, 'Brand': Brand, 'UploadFile': UploadFile}