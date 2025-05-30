from models import db

class GradoMateria(db.Model):
    __tablename__ = 'grado_materia'
    id = db.Column(db.Integer, primary_key=True)

    grado_id = db.Column(db.Integer, db.ForeignKey('grado.id'), nullable=False)
    materia_base_id = db.Column(db.Integer, db.ForeignKey('materia_base.id'), nullable=False)

    turno = db.Column(db.String(20), nullable=True)   # Opcional
    aula = db.Column(db.String(100), nullable=True)   # Opcional
    estado = db.Column(db.String(20), nullable=True)  # activo / inactivo

    grado = db.relationship('Grado', backref='grado_materias')
    materia_base = db.relationship('MateriaBase', backref='grado_materias')
