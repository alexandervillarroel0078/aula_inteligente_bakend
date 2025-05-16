from models import db

class MateriaProfesor(db.Model):
    __tablename__ = 'materia_profesor'
    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesor.id'))
    fecha_asignacion = db.Column(db.Date)

    materia = db.relationship('Materia', backref='materia_profesores')
    profesor = db.relationship('Profesor', backref='materia_profesores')
