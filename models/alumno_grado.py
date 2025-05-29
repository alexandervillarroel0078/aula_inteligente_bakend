from models import db
from sqlalchemy import CheckConstraint

class AlumnoGrado(db.Model):
    __tablename__ = 'alumno_grado'

    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'), primary_key=True)  # ID del alumno
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'), primary_key=True)    # ID del grado

    gestion = db.Column(db.Integer, nullable=False)                                   # Año escolar
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())      # Fecha automática

    estado = db.Column(db.String(20), nullable=False, default='pendiente')            # Estado del alumno en el grado

    # Relaciones con modelos
    alumno = db.relationship('Alumno', backref=db.backref('alumno_grados', lazy=True))  # Relación con Alumno
    grado = db.relationship('Grado', backref=db.backref('grado_alumnos', lazy=True))    # Relación con Grado

    # Restricciones y mejoras
    __table_args__ = (
        CheckConstraint(  # ✅ Solo permite estados válidos
            "estado IN ('pendiente', 'en curso', 'aprobado', 'no aprobado')",
            name='check_estado_valido'
        ),
        db.Index('ix_grado_gestion', 'grado_id', 'gestion'),  # 🚀 Acelera consultas por grado + gestión
    )

    # def __repr__(self):
    #     return f'<AlumnoGrado alumno_id={self.alumno_id} grado_id={self.grado_id}>'  # 🧾 Para debug/print

    # def to_dict(self):
    #     return {  # 📤 Facilita conversión a JSON
    #         "alumno_id": self.alumno_id,
    #         "grado_id": self.grado_id,
    #         "gestion": self.gestion,
    #         "estado": self.estado,
    #         "fecha_registro": self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
    #     }
