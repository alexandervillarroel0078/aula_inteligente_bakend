from flask import jsonify
from models import db
from models.usuario import Usuario

def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([
        {
            "id": u.id,
            "nombre_usuario": u.nombre_usuario,
            "rol_id": u.rol_id,
            "rol_nombre": u.rol.nombre if u.rol else None,
            "profesor_id": u.profesor_id,
            "profesor_nombre": u.profesor.nombre_completo if u.profesor else None,
            "alumno_id": u.alumno_id,
            "alumno_nombre": u.alumno.nombre_completo if u.alumno else None
        } for u in usuarios
    ])

def obtener_usuario(id):
    u = Usuario.query.get_or_404(id)
    return jsonify({
        "id": u.id,
        "nombre_usuario": u.nombre_usuario,
        "rol_id": u.rol_id,
        "rol_nombre": u.rol.nombre if u.rol else None,
        "profesor_id": u.profesor_id,
        "profesor_nombre": u.profesor.nombre_completo if u.profesor else None,
        "alumno_id": u.alumno_id,
        "alumno_nombre": u.alumno.nombre_completo if u.alumno else None
    })

def crear_usuario(request):
    data = request.get_json()
    nuevo = Usuario(
        nombre_usuario=data.get('nombre_usuario'),
        password_hash=data.get('password_hash'),  # debe estar previamente encriptado
        rol_id=data.get('rol_id'),
        profesor_id=data.get('profesor_id'),
        alumno_id=data.get('alumno_id')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado con éxito"}), 201

def actualizar_usuario(id, request):
    u = Usuario.query.get_or_404(id)
    data = request.get_json()

    u.nombre_usuario = data.get('nombre_usuario', u.nombre_usuario)
    u.password_hash = data.get('password_hash', u.password_hash)
    u.rol_id = data.get('rol_id', u.rol_id)
    u.profesor_id = data.get('profesor_id', u.profesor_id)
    u.alumno_id = data.get('alumno_id', u.alumno_id)

    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado con éxito"})

def eliminar_usuario(id):
    u = Usuario.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado con éxito"})
