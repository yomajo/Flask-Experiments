from config import DevelopmentConfig
from flask import Flask, render_template
from app.routes import bp
from app.models import db



def create_app():

    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config.from_object(DevelopmentConfig)    

    from app.models import db
    db.init_app(app)

    return app
