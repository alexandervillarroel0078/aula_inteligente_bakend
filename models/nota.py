from models import db

class Nota(db.Model):
    __tablename__ = 'nota'
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    nota_final = db.Column(db.Float)
    observaciones = db.Column(db.Text)
