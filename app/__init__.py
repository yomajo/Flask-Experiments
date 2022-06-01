from config import DevelopmentConfig
from flask import Flask, render_template
from app.routes import site
from app.routes.products import prod_bp
from app.routes.users import roles_bp
from app.models import db



def create_app():

    app = Flask(__name__)
    app.register_blueprint(site)
    app.register_blueprint(prod_bp)
    app.register_blueprint(roles_bp)

    app.config.from_object(DevelopmentConfig)    

    from app.models import db
    db.init_app(app)

    return app
