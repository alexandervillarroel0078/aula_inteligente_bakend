# models/bitacora.py
from models import db
from datetime import datetime

class Bitacora(db.Model):
    __tablename__ = 'bitacora'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    accion = db.Column(db.String(255), nullable=False)
    tabla = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(50))  # ← nuevo campo
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref='bitacoras')
