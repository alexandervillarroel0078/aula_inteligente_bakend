from flask import jsonify
from models import db
from models.tarea import Tarea
from traits.bitacora_trait import registrar_bitacora

def listar_tareas():
    tareas = Tarea.query.all()
    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "descripcion": t.descripcion,
            "fecha_entrega": t.fecha_entrega.isoformat() if t.fecha_entrega else None,
            "materia_id": t.materia_id,
            "materia_nombre": t.materia.nombre if t.materia else None,
            "profesor_id": t.profesor_id,
            "profesor_nombre": t.profesor.nombre_completo if t.profesor else None
        }
        for t in tareas
    ])


def ver_tarea(id):
    t = Tarea.query.get_or_404(id)
    return jsonify({
        "id": t.id,
        "titulo": t.titulo,
        "descripcion": t.descripcion,
        "fecha_entrega": t.fecha_entrega,
        "materia_id": t.materia_id,
        "profesor_id": t.profesor_id
    })

def crear_tarea(request):
    data = request.get_json()
    nueva = Tarea(
        titulo = data['titulo'],
        descripcion = data['descripcion'],
        fecha_entrega = data['fecha_entrega'],
        materia_id = data['materia_id'],
        profesor_id = data['profesor_id']
    )
    db.session.add(nueva)
    db.session.commit()
    registrar_bitacora("tarea", f"creó tarea ID {nueva.id}")
    return jsonify({"mensaje": "Tarea creada correctamente", "id": nueva.id})

def editar_tarea(id, request):
    t = Tarea.query.get_or_404(id)
    data = request.get_json()

    t.titulo = data['titulo']
    t.descripcion = data['descripcion']
    t.fecha_entrega = data['fecha_entrega']
    t.materia_id = data['materia_id']
    t.profesor_id = data['profesor_id']

    db.session.commit()
    registrar_bitacora("tarea", f"editó tarea ID {t.id}")
    return jsonify({"mensaje": "Tarea actualizada correctamente"})

def eliminar_tarea(id):
    t = Tarea.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    registrar_bitacora("tarea", f"eliminó tarea ID {id}")
    return jsonify({"mensaje": "Tarea eliminada correctamente"})
