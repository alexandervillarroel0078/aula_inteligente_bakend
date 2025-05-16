from models import db

class Profesor(db.Model):
    __tablename__ = 'profesor'
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    especialidad = db.Column(db.String(100))
    estado = db.Column(db.String(20))
