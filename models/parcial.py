from models import db

class Parcial(db.Model):
    __tablename__ = 'parcial'
    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'), nullable=False)

    parcial = db.Column(db.Float, nullable=False)

    alumno = db.relationship('Alumno', backref='parciales')
    materia = db.relationship('Materia', backref='parciales')
    periodo = db.relationship('Periodo', backref='parciales')
