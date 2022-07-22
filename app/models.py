from datetime import datetime
from flask_login import UserMixin
from .extensions import db, login_manager
from sqlalchemy import ForeignKey

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

class SKU(db.Model):
    __tablename__ = 'sku'

    sku = db.Column(db.String(100), primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    same_weight_lsts = db.Column(db.Boolean, default=True)

    upload_id = db.Column(db.Integer, ForeignKey('uploadfile.id'))
    file = db.relationship('UploadFile')

    def __repr__(self) -> str:
        return f'SKU(sku={self.sku}, same_weight_lsts={self.same_weight_lsts}, upload_id={self.upload_id})'
    

class UploadFile(db.Model):
    __tablename__ = 'uploadfile'

    id = db.Column(db.Integer, primary_key=True)
    fpath = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'''UploadFile(id={self.id},
            fpath={self.fpath},
            upload_date={self.upload_date})'''
