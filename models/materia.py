from models import db

class Materia(db.Model):
    __tablename__ = 'materia'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'))
    estado = db.Column(db.String(20))

    grado = db.relationship('Grado', backref='materias')
