from config import DevelopmentConfig
from flask import Flask
from flask_migrate import Migrate
from app.routes import site
from app.routes.products import prod_bp
from app.routes.users import roles_bp
from app.routes.files import files_bp
from app.extensions import login_manager, search


def create_app():

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(site)
    app.register_blueprint(prod_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(files_bp)

    from app.extensions import db
    db.init_app(app)
    Migrate(app, db)
    search.init_app(app)
    

    login_manager.init_app(app)

    return app
