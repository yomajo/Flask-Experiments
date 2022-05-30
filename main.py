from app.models import db
from app import create_app


app = create_app()

# @app.cli.command()
# def createdb():
#     db.create_all()