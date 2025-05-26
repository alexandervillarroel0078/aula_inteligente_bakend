from models import db

class Periodo(db.Model):
    __tablename__ = 'periodo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(20))
    semestre = db.Column(db.String(20))
    anio = db.Column(db.Integer)
    codigoPeriodo = db.Column(db.String(20), unique=True)
    
    # Relación con Grado, donde grado_id es la clave foránea
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'))  # Relación con 'grado'
    grado = db.relationship('Grado', backref=db.backref('periodos', lazy=True))  # Relación inversa
