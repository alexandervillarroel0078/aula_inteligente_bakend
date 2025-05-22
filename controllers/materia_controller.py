from flask import jsonify
from models import db
from models.materia import Materia

def listar_materias():
    materias = Materia.query.all()
    return jsonify([
        {
            "id": m.id,
            "nombre": m.nombre,
            "descripcion": m.descripcion,
            "grado_id": m.grado_id,
            "grado_nombre": m.grado.nombre if m.grado else None,  # ← agregado
            "estado": m.estado
        } for m in materias
    ])

def obtener_materia(id):
    materia = Materia.query.get_or_404(id)
    return jsonify({
        "id": materia.id,
        "nombre": materia.nombre,
        "descripcion": materia.descripcion,
        "grado_id": materia.grado_id,
        "grado_nombre": materia.grado.nombre if materia.grado else None,  # ← agregado
        "estado": materia.estado
    })

def crear_materia(request):
    data = request.get_json()
    nueva = Materia(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        grado_id=data.get('grado_id'),
        estado=data.get('estado')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Materia creada con éxito"}), 201

def actualizar_materia(id, request):
    materia = Materia.query.get_or_404(id)
    data = request.get_json()

    materia.nombre = data.get('nombre', materia.nombre)
    materia.descripcion = data.get('descripcion', materia.descripcion)
    materia.grado_id = data.get('grado_id', materia.grado_id)
    materia.estado = data.get('estado', materia.estado)

    db.session.commit()
    return jsonify({"mensaje": "Materia actualizada con éxito"})

def eliminar_materia(id):
    materia = Materia.query.get_or_404(id)
    db.session.delete(materia)
    db.session.commit()
    return jsonify({"mensaje": "Materia eliminada con éxito"})
