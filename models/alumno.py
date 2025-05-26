from models import db

class Alumno(db.Model):
    __tablename__ = 'alumno'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)  # Ej: ALU-001
    nombre_completo = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(10))
    fecha_registro = db.Column(db.DateTime)
    estado = db.Column(db.String(20))  # activo / inactivo
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
  
    #grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'))  # Relación
    #grado = db.relationship('Grado', backref='alumnos')
