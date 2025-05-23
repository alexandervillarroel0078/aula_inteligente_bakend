from models import db

class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id = db.Column(db.Integer, primary_key=True)
   
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    
    fecha = db.Column(db.Date)
    presente = db.Column(db.Boolean)

    # Relaciones necesarias para acceder a los nombres
    alumno = db.relationship('Alumno', backref='asistencias')
    materia = db.relationship('Materia', backref='asistencias')
    periodo = db.relationship('Periodo', backref='asistencias')
