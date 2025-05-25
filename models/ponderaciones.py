from models import db

class Ponderacion(db.Model):
    __tablename__ = 'ponderacion'
    id = db.Column(db.Integer, primary_key=True)
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'), nullable=False)
    parcial = db.Column(db.Float, nullable=False)          # Porcentaje del parcial
    asistencia = db.Column(db.Float, nullable=False)       # Porcentaje de la asistencia
    participacion = db.Column(db.Float, nullable=False)    # Porcentaje de la participación

    # Relación con el modelo Grado
    grado = db.relationship('Grado', backref=db.backref('ponderaciones', lazy=True))

    def __repr__(self):
        return f'<Ponderacion grado_id={self.grado_id} parcial={self.parcial} asistencia={self.asistencia} participacion={self.participacion}>'
