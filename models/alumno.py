from models import db

class Alumno(db.Model):
    __tablename__ = 'alumno'
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(10))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'))
    fecha_registro = db.Column(db.DateTime)
    estado = db.Column(db.String(20))

    #relación directa
    grado = db.relationship('Grado', backref='alumnos')
