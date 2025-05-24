from models import db

class Periodo(db.Model):
    __tablename__ = 'periodo'
    id = db.Column(db.Integer, primary_key=True)
    #nombre = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(50))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(20))

    # Nuevos campos
    semestre = db.Column(db.String(20))  # Ej: "1er Semestre", "2do Semestre"
    anio = db.Column(db.Integer)         # Ej: 2024
