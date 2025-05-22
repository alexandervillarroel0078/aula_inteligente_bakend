from models import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(100))  # ✅ agrega este campo
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesor.id'), nullable=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'), nullable=True)

    rol = db.relationship('Rol', backref='usuarios')
    profesor = db.relationship('Profesor', backref='usuario', uselist=False)
    alumno = db.relationship('Alumno', backref='usuario', uselist=False)
