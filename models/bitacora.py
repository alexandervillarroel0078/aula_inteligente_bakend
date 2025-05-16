from models import db

class Bitacora(db.Model):
    __tablename__ = 'bitacora'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    accion = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    fecha_hora = db.Column(db.DateTime)
