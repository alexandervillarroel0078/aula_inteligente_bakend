from models import db

class Profesor(db.Model):
    __tablename__ = 'profesor'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)  # ← nuevo campo
    nombre_completo = db.Column(db.String(100), nullable=False)
    ci = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    estado = db.Column(db.String(20))
