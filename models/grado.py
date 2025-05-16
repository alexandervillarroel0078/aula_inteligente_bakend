from models import db

class Grado(db.Model):
    __tablename__ = 'grado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nivel = db.Column(db.String(50))
    turno = db.Column(db.String(20))
