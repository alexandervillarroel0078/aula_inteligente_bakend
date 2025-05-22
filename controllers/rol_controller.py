from flask import jsonify
from models import db
from models.rol import Rol

def listar_roles():
    roles = Rol.query.all()
    return jsonify([
        {
            "id": r.id,
            "nombre": r.nombre,
            "descripcion": r.descripcion
        } for r in roles
    ])

def obtener_rol(id):
    r = Rol.query.get_or_404(id)
    return jsonify({
        "id": r.id,
        "nombre": r.nombre,
        "descripcion": r.descripcion
    })

def crear_rol(request):
    data = request.get_json()
    nuevo = Rol(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Rol creado con éxito"}), 201

def actualizar_rol(id, request):
    r = Rol.query.get_or_404(id)
    data = request.get_json()

    r.nombre = data.get('nombre', r.nombre)
    r.descripcion = data.get('descripcion', r.descripcion)

    db.session.commit()
    return jsonify({"mensaje": "Rol actualizado con éxito"})

def eliminar_rol(id):
    r = Rol.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"mensaje": "Rol eliminado con éxito"})
