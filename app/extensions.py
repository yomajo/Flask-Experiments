from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_msearch import Search

db = SQLAlchemy()
login_manager = LoginManager()
search = Search()