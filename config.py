from dotenv import load_dotenv
import os

# load environment variables
load_dotenv('.env')

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    UPLOAD_FOLDER = 'static/uploads'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    PG_PASS = os.environ['PG_PASS']

    PG_USER='yo'
    PG_DB='flaskexperiments'
    PG_HOST='localhost'
    PG_PORT='5432'

    SECRET_KEY = 'supersecretstuff'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}'


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True