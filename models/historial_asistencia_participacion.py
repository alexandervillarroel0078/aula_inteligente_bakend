from models import db

class HistorialAsistenciaParticipacion(db.Model):
    __tablename__ = 'historial_asistencia_participacion'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'))
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'))
    
    gestion = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50))  # "asistencia" o "participacion"
    puntaje = db.Column(db.Float, nullable=True)  # Solo para la participación y asistnecia
    fecha = db.Column(db.Date)
    observaciones = db.Column(db.Text, nullable=True)

    # Relaciones
    alumno = db.relationship('Alumno', backref='historial_asistencia_participacion')
    materia = db.relationship('Materia', backref='historial_asistencia_participacion')
    periodo = db.relationship('Periodo', backref='historial_asistencia_participacion')
    grado = db.relationship('Grado', backref='historial_asistencia_participacion')

    def __repr__(self):
        return f"<HistorialAsistenciaParticipacion id={self.id} alumno_id={self.alumno_id} tipo={self.tipo}>"
