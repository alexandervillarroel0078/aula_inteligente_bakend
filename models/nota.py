from models import db
from models.alumno import Alumno
from models.materia import Materia
from models.periodo import Periodo

class Nota(db.Model):
    __tablename__ = 'nota'
    id = db.Column(db.Integer, primary_key=True)
   
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    
   # nota_final = db.Column(db.Float)
    nota_final = db.Column(db.Float, nullable=False)
    observaciones = db.Column(db.Text)

    # 🔧 Relaciones necesarias para usar n.alumno, n.materia, n.periodo
    alumno = db.relationship('Alumno', backref='notas')
    materia = db.relationship('Materia', backref='notas')
    periodo = db.relationship('Periodo', backref='notas')
