from dotenv import load_dotenv
import os

# load environment variables
load_dotenv('.env')

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    # broker_url = 'redis://127.0.0.1:6379/0',
    # result_backend = 'redis://127.0.0.1:6379/0'



class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    PG_PASS = os.environ['PG_PASS']

    PG_USER='yo'
    PG_DB='flaskexperiments'
    PG_HOST='localhost'
    PG_PORT='5432'

    SECRET_KEY = 'supersecretstuff'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}'

    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

    # CELERY_CONFIG = {
    #     'broker_url': 'redis://localhost:6379/0',
    #     'result_backend': 'redis://localhost:6379/0'
    #     }
    

class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

