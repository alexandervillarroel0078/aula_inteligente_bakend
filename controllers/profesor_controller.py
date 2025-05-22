from flask import jsonify
from models import db
from models.profesor import Profesor

def listar_profesores():
    profesores = Profesor.query.all()
    return jsonify([{
        "id": p.id,
        "nombre_completo": p.nombre_completo,
        "email": p.email,
        "telefono": p.telefono,
        "direccion": p.direccion,
        "especialidad": p.especialidad,
        "estado": p.estado
    } for p in profesores])

def obtener_profesor(id):
    profesor = Profesor.query.get_or_404(id)
    return jsonify({
        "id": profesor.id,
        "nombre_completo": profesor.nombre_completo,
        "email": profesor.email,
        "telefono": profesor.telefono,
        "direccion": profesor.direccion,
        "especialidad": profesor.especialidad,
        "estado": profesor.estado
    })

def crear_profesor(request):
    data = request.get_json()
    nuevo = Profesor(
        nombre_completo=data.get('nombre_completo'),
        email=data.get('email'),
        telefono=data.get('telefono'),
        direccion=data.get('direccion'),
        especialidad=data.get('especialidad'),
        estado=data.get('estado')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Profesor creado con éxito"}), 201

def actualizar_profesor(id, request):
    profesor = Profesor.query.get_or_404(id)
    data = request.get_json()

    profesor.nombre_completo = data.get('nombre_completo', profesor.nombre_completo)
    profesor.email = data.get('email', profesor.email)
    profesor.telefono = data.get('telefono', profesor.telefono)
    profesor.direccion = data.get('direccion', profesor.direccion)
    profesor.especialidad = data.get('especialidad', profesor.especialidad)
    profesor.estado = data.get('estado', profesor.estado)

    db.session.commit()
    return jsonify({"mensaje": "Profesor actualizado con éxito"})

def eliminar_profesor(id):
    profesor = Profesor.query.get_or_404(id)
    db.session.delete(profesor)
    db.session.commit()
    return jsonify({"mensaje": "Profesor eliminado con éxito"})
