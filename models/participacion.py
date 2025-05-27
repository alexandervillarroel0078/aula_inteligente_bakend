from models import db

class Participacion(db.Model):
    __tablename__ = 'participacion'
    id = db.Column(db.Integer, primary_key=True)
    
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'), nullable=False)

    # Relaciones necesarias
    alumno = db.relationship('Alumno', backref='participaciones')
    materia = db.relationship('Materia', backref='participaciones')
    periodo = db.relationship('Periodo', backref='participaciones')
    grado = db.relationship('Grado', backref='participaciones')
    
    gestion = db.Column(db.Integer, nullable=False)
    cantidad_participacion = db.Column(db.Integer, nullable=False)  # Contador de participaciones
    nota_participacion = db.Column(db.Float, nullable=True)  
    observaciones = db.Column(db.Text, nullable=True)