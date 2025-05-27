from models import db

class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'))  
   
    alumno = db.relationship('Alumno', backref='asistencias')
    materia = db.relationship('Materia', backref='asistencias')
    periodo = db.relationship('Periodo', backref='asistencias')
    grado = db.relationship('Grado', backref=db.backref('asistencias')) 
   
    
    gestion = db.Column(db.Integer, nullable=False)
    nota_asistencia = db.Column(db.Float, nullable=False)  
    observaciones = db.Column(db.Text, nullable=True)
