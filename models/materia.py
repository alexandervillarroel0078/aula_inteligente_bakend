from models import db

class Materia(db.Model):
    __tablename__ = 'materia'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)  # ej. MAT-1A-MA
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    turno = db.Column(db.String(20))  # Mañana / Tarde
    aula = db.Column(db.String(100))  # Aula 1, Lab, etc.
    estado = db.Column(db.String(20))  # activo / inactivo

    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'))  # Relación
    grado = db.relationship('Grado', backref='materias')

     