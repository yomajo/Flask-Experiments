from datetime import datetime
from flask_login import UserMixin
from .extensions import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    # no no in production
    password = db.Column(db.String(50), unique=True, nullable=False)
    # clearance: 1 - Admin; 2 - Manager; 3 - average Joe
    clearance = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'User(id={self.id}, name={self.name}, password={self.password}, clearance={self.clearance})'    


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    qty = db.Column(db.Integer, nullable=False)
    brand_name = db.Column(db.String(20), db.ForeignKey('brand.name'))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f'Products(id={self.id}, name={self.name}, qty={self.qty})'

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    products = db.relationship('Products', backref='brand')
    
    def __repr__(self) -> str:
        return f'Brand(id={self.id}, name={self.name})'

class UploadFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(30), nullable=False)
    fpath = db.Column(db.String(100), nullable=False)
    user_upload = db.Column(db.Boolean)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'''UploadFile(id={self.id},
            filename={self.filename},
            fpath={self.fpath},
            user_upload={self.user_upload},
            upload_date={self.upload_date})'''
