from models import db

class MateriaProfesor(db.Model):
    __tablename__ = 'materia_profesor'
    
    id = db.Column(db.Integer, primary_key=True)
    
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'))
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesor.id'))
    
    fecha_asignacion = db.Column(db.Date)
    gestion = db.Column(db.Integer, nullable=False)
    
    # Agregar estado para gestionar la asignación
    estado = db.Column(db.String(20), default='activo')  # Puede ser 'activo', 'inactivo', etc.
    
    materia = db.relationship('Materia', backref='materia_profesores')
    profesor = db.relationship('Profesor', backref='materia_profesores')

    def __repr__(self):
        return f'<MateriaProfesor id={self.id} materia_id={self.materia_id} profesor_id={self.profesor_id} estado={self.estado}>'
