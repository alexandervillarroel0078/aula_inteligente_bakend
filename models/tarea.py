from models import db

class Tarea(db.Model):
    __tablename__ = 'tarea'
    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesor.id'))
    titulo = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    fecha_entrega = db.Column(db.Date)

    # Relaciones necesarias
    materia = db.relationship('Materia', backref='tareas')
    profesor = db.relationship('Profesor', backref='tareas')
