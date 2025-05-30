# models/gestion.py

from . import db

class Gestion(db.Model):
    __tablename__ = 'gestiones'

    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Integer, nullable=False, unique=True)  # Ej: 2025
    descripcion = db.Column(db.String(100))  # Opcional, como "Gestión Escolar 2025"
    estado = db.Column(db.String(20), default='activa')  # activa, finalizada, futura, etc.

    def __repr__(self):
        return f'<Gestion {self.anio}>'
