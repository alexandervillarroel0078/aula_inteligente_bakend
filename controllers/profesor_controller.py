from flask import jsonify
from models import db
from models.profesor import Profesor
from traits.bitacora_trait import registrar_bitacora

def listar_profesores():
    profesores = Profesor.query.all()
    return jsonify([
        {
            "id": p.id,
            "codigo": p.codigo,
            "nombre_completo": p.nombre_completo,
            "ci": p.ci,
            "email": p.email,
            "telefono": p.telefono,
            "direccion": p.direccion,
            "estado": p.estado
        } for p in profesores
    ])

def ver_profesor(id):
    p = Profesor.query.get_or_404(id)
    return jsonify({
        "id": p.id,
        "codigo": p.codigo,
        "nombre_completo": p.nombre_completo,
        "ci": p.ci,
        "email": p.email,
        "telefono": p.telefono,
        "direccion": p.direccion,
        "estado": p.estado
    })

def crear_profesor(request):
    data = request.get_json()
    nuevo = Profesor(
        codigo = data['codigo'],
        nombre_completo = data['nombre_completo'],
        ci = data['ci'],
        email = data['email'],
        telefono = data['telefono'],
        direccion = data['direccion'],
        estado = data['estado']
    )
    db.session.add(nuevo)
    db.session.commit()
    registrar_bitacora("profesor", f"creó profesor ID {nuevo.id}")
    return jsonify({"mensaje": "Profesor registrado correctamente", "id": nuevo.id})

def editar_profesor(id, request):
    p = Profesor.query.get_or_404(id)
    data = request.get_json()

    p.codigo = data['codigo']
    p.nombre_completo = data['nombre_completo']
    p.ci = data['ci']
    p.email = data['email']
    p.telefono = data['telefono']
    p.direccion = data['direccion']
    p.estado = data['estado']

    db.session.commit()
    registrar_bitacora("profesor", f"editó profesor ID {p.id}")
    return jsonify({"mensaje": "Profesor actualizado correctamente"})

def eliminar_profesor(id):
    p = Profesor.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    registrar_bitacora("profesor", f"eliminó profesor ID {id}")
    return jsonify({"mensaje": "Profesor eliminado correctamente"})
