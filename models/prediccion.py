from models import db

class Prediccion(db.Model):
    __tablename__ = 'prediccion'
    id = db.Column(db.Integer, primary_key=True)
    
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id')) 
    
    promedio_notas = db.Column(db.Float)
    porcentaje_asistencia = db.Column(db.Float)
    promedio_participaciones = db.Column(db.Float)
    resultado_predicho = db.Column(db.Float)


    # Relaciones necesarias
    alumno = db.relationship('Alumno', backref='predicciones')
    periodo = db.relationship('Periodo', backref='predicciones')
    materia = db.relationship('Materia', backref='predicciones')