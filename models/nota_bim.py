from models import db
from models.alumno import Alumno
from models.materia import Materia
from models.periodo import Periodo
from models.grado import Grado 

class Nota(db.Model):
    __tablename__ = 'nota'

    # ID único de la nota
    id = db.Column(db.Integer, primary_key=True)

    # Relaciones con otras tablas
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'))

    # Atributos adicionales
    tipo_parcial = db.Column(db.String(50), nullable=False)  # Ej: "Primer Parcial", "Segundo Parcial", etc.
    observaciones = db.Column(db.Text)

    grado_nombre = db.Column(db.String(100), nullable=False)  # Nombre del grado, ej: "1ro A"
    gestion = db.Column(db.Integer, nullable=False)  # Año del grado

    # Nuevas columnas para participación y asistencia
    nota = db.Column(db.Float, nullable=False)  # Nota por parcial
    nota_participacion = db.Column(db.Float, nullable=True)  # Nota de participación
    nota_asistencia = db.Column(db.Float, nullable=True)  # Nota de asistencia

    # Relaciones
    alumno = db.relationship('Alumno', backref='notas')
    materia = db.relationship('Materia', backref='notas')
    periodo = db.relationship('Periodo', backref='notas')
    grado = db.relationship('Grado', backref='notas')

    def __repr__(self):
        return f"<Nota id={self.id} alumno_id={self.alumno_id} materia_id={self.materia_id} periodo_id={self.periodo_id} grado_id={self.grado_id}>"
