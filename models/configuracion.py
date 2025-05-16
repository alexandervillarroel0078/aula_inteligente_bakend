from models import db

class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), unique=True)
    valor = db.Column(db.String(255))
    descripcion = db.Column(db.String(255))
