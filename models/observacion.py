from models import db

class Observacion(db.Model):
    __tablename__ = 'observacion'
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesor.id'))
    fecha = db.Column(db.Date)
    descripcion = db.Column(db.Text)
