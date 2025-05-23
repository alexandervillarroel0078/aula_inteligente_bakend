from models import db

class Grado(db.Model):
    __tablename__ = 'grado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)          # Ej: "1ro A"
    nivel = db.Column(db.String(50), nullable=False)            # Primaria / Secundaria
    seccion = db.Column(db.String(50), nullable=True)           # Primero / Segundo...
    paralelo = db.Column(db.String(10), nullable=True)          # A, B, C
    turno = db.Column(db.String(50), nullable=False)            # Mañana / Tarde
    gestion = db.Column(db.Integer, nullable=False)             # Año escolar
    ubicacion = db.Column(db.String(100), nullable=True)        # Sede o sucursal   