from models import db

class TareaEntregada(db.Model):
    __tablename__ = 'tarea_entregada'

    id = db.Column(db.Integer, primary_key=True)
    archivo_url = db.Column(db.String(255))
    fecha_entrega = db.Column(db.Date)
    calificacion = db.Column(db.Float)

    tarea_id = db.Column(db.Integer, db.ForeignKey('tarea.id'))
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    # Relaciones necesarias
    tarea = db.relationship('Tarea', backref='entregas')
    alumno = db.relationship('Alumno', backref='entregas_tarea')
