from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    qty = db.Column(db.Integer, nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f'Products(id={self.id}, name={self.name}, qty={self.qty})'