from config import DevelopmentConfig
from flask import Flask, render_template
from app.routes import bp
from app.models import db

from fastapi import FastAPI
from app.endpoints import router
from config import DevSettingsForFastAPI



def create_app():
    api = FastAPI()
    settings = DevSettingsForFastAPI()
    api.include_router(router)

    # app = Flask(__name__)
    # app.register_blueprint(bp)
    # app.config.from_object(DevelopmentConfig)    

    # from app.models import db
    # db.init_app(app)

    # return app
    return api
