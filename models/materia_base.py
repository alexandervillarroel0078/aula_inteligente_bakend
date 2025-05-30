from models import db

class MateriaBase(db.Model):
    __tablename__ = 'materia_base'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
