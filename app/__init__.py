from config import Config, DevelopmentConfig
from flask import Flask
from flask_migrate import Migrate
from app.routes import site
from app.routes.products import prod_bp
from app.routes.users import roles_bp
from app.routes.files import files_bp
from app.routes.tasks import tasks_bp
from app.extensions import login_manager
from celeryconfig import broker_url
from celery import Celery


celery_in = Celery(__name__, broker=broker_url)


def create_app():

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)    

    app.register_blueprint(site)
    app.register_blueprint(prod_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(tasks_bp)

    from app.extensions import db
    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)
    # celery_in.conf.update(app.config)

    return app
