from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    # no no in production
    password = db.Column(db.String(50), unique=True, nullable=False)
    # clearance: 1 - Admin; 2 - Manager; 3 - average Joe
    clearance = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'Products(id={self.id}, name={self.name}, password={self.password}, clearance={self.clearance})'    


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    qty = db.Column(db.Integer, nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f'Products(id={self.id}, name={self.name}, qty={self.qty})'