from models import db

class Observacion(db.Model):
    __tablename__ = 'observacion'
    id = db.Column(db.Integer, primary_key=True)

    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesor.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))  # ← Agregado

    fecha = db.Column(db.Date)
    descripcion = db.Column(db.Text)

    # Relaciones
    alumno = db.relationship('Alumno', backref='observaciones')
    profesor = db.relationship('Profesor', backref='observaciones')
    periodo = db.relationship('Periodo', backref='observaciones')
