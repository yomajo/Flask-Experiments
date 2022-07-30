from config import DevelopmentConfig
from flask import Flask
from flask_migrate import Migrate
from app.routes import site
from app.routes.products import prod_bp
from app.routes.users import roles_bp
from app.routes.files import files_bp
from app.routes.search import search_bp

from app.models import Products
from app.extensions import login_manager
import flask_whooshalchemy3 as wa

# wa.DEFAULT_WHOOSH_INDEX_PATH = 'whoosh'


def create_app():

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(site)
    app.register_blueprint(prod_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(search_bp)

    from app.extensions import db
    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)
    try:
        wa.create_index(app, Products, name='whoosh')
    except AssertionError:
        print(f'Failed to get whoosh index. Working outside of request context?')

    return app
