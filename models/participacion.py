from models import db

class Participacion(db.Model):
    __tablename__ = 'participacion'
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    fecha = db.Column(db.Date)
    puntaje = db.Column(db.Float)

    # Relaciones necesarias
    alumno = db.relationship('Alumno', backref='participaciones')
    materia = db.relationship('Materia', backref='participaciones')
    periodo = db.relationship('Periodo', backref='participaciones')
