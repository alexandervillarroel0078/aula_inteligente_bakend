from flask import jsonify
from models import db
from models.usuario import Usuario
from traits.bitacora_trait import registrar_bitacora

# GET - Listar usuarios
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([
        {
            "id": u.id,
            "nombre_usuario": u.nombre_usuario,
            "correo": u.correo,
            "rol_id": u.rol_id,
            "rol_nombre": u.rol.nombre if u.rol else None,
            "profesor_id": u.profesor_id,
            "profesor_nombre": u.profesor.nombre_completo if u.profesor else None,
            "alumno_id": u.alumno_id,
            "alumno_nombre": u.alumno.nombre_completo if u.alumno else None
        } for u in usuarios
    ])


# GET - Ver un usuario
def ver_usuario(id):
    u = Usuario.query.get_or_404(id)
    return jsonify({
        "id": u.id,
        "nombre_usuario": u.nombre_usuario,
        "correo": u.correo,
        "rol_id": u.rol_id,
        "profesor_id": u.profesor_id,
        "alumno_id": u.alumno_id
    })

# POST - Crear nuevo usuario
def crear_usuario(request):
    data = request.get_json()
    nuevo = Usuario(
        nombre_usuario = data['nombre_usuario'],
        password_hash = data['password_hash'],
        correo = data.get('correo'),
        rol_id = data['rol_id'],
        profesor_id = data.get('profesor_id'),
        alumno_id = data.get('alumno_id')
    )
    db.session.add(nuevo)
    db.session.commit()
    registrar_bitacora("usuario", f"creó usuario ID {nuevo.id}")
    return jsonify({"mensaje": "Usuario creado correctamente", "id": nuevo.id})

# PUT - Editar usuario
def editar_usuario(id, request):
    u = Usuario.query.get_or_404(id)
    data = request.get_json()

    u.nombre_usuario = data['nombre_usuario']
    u.password_hash = data['password_hash']
    u.correo = data.get('correo')
    u.rol_id = data['rol_id']
    u.profesor_id = data.get('profesor_id')
    u.alumno_id = data.get('alumno_id')

    db.session.commit()
    registrar_bitacora("usuario", f"editó usuario ID {u.id}")
    return jsonify({"mensaje": "Usuario actualizado correctamente"})

# DELETE - Eliminar usuario
def eliminar_usuario(id):
    u = Usuario.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    registrar_bitacora("usuario", f"eliminó usuario ID {id}")
    return jsonify({"mensaje": "Usuario eliminado correctamente"})
