from models import db

class Periodo(db.Model):
    __tablename__ = 'periodo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(20))
