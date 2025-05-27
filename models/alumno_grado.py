from models import db

class AlumnoGrado(db.Model):
    __tablename__ = 'alumno_grado'
    
    # El campo 'alumno_id' es un entero y hace referencia a la clave primaria 'id' de la tabla 'Alumno'
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'), primary_key=True)
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'), primary_key=True)
    
    gestion = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relación con los modelos Alumno y Grado
    alumno = db.relationship('Alumno', backref=db.backref('alumno_grados', lazy=True))
    grado = db.relationship('Grado', backref=db.backref('grado_alumnos', lazy=True))
    
    estado = db.Column(db.String(20), nullable=False, default='pendiente')  # 'pendiente', 'aprobado', 'no aprobado'

    def __repr__(self):
        return f'<AlumnoGrado alumno_id={self.alumno_id} grado_id={self.grado_id}>'
