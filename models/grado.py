from models import db

class Grado(db.Model):
    __tablename__ = 'grado'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)          # Ej: "1ro A"
    descripcion = db.Column(db.String(255), nullable=True)
    
    nivel = db.Column(db.String(50), nullable=False)            # Primaria / Secundaria
    seccion = db.Column(db.String(50), nullable=True)           # Primero / Segundo...
    paralelo = db.Column(db.String(10), nullable=True)          # A, B, C
    turno = db.Column(db.String(50), nullable=False)            # Mañana / Tarde
    ubicacion = db.Column(db.String(100), nullable=True)        # Sede o sucursal   
    codigoGrado = db.Column(db.String(20), unique=True)         # Ej: "1A22"
    
    gestion_id = db.Column(db.Integer, db.ForeignKey('gestiones.id'), nullable=False)
    gestion = db.relationship('Gestion', backref='grados')