from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


# celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

# def make_celery(app):
#     celery = Celery(app.import_name)
#     celery.conf.broker_url = app.config['BROKER_URL']
#     celery.conf.result_backend = app.config['RESULT_BACKEND']    
#     celery.conf.update(app.config)

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery