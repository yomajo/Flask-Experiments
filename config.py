from dotenv import load_dotenv
import os

# load environment variables
load_dotenv('.env')

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    # PG_PASS = os.environ['PG_PASS']

    # PG_USER='yo'
    # PG_DB='flaskexperiments'
    # PG_HOST='localhost'
    # PG_PORT='5432'

    # SECRET_KEY = 'supersecretstuff'
    # SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'

    MSEARCH_INDEX_NAME = 'msearch'
    # simple,whoosh,elaticsearch, default is simple
    MSEARCH_BACKEND = 'whoosh'
    # table's primary key if you don't like to use id, or set __msearch_primary_key__ for special model
    MSEARCH_PRIMARY_KEY = 'id'
    # auto create or update index
    MSEARCH_ENABLE = True


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True