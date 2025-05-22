from flask import jsonify
from models import db
from models.tarea import Tarea

def listar_tareas():
    tareas = Tarea.query.all()
    return jsonify([
        {
            "id": t.id,
            "materia_id": t.materia_id,
            "materia_nombre": t.materia.nombre if t.materia else None,
            "profesor_id": t.profesor_id,
            "profesor_nombre": t.profesor.nombre_completo if t.profesor else None,
            "titulo": t.titulo,
            "descripcion": t.descripcion,
            "fecha_entrega": t.fecha_entrega.isoformat() if t.fecha_entrega else None
        } for t in tareas
    ])

def obtener_tarea(id):
    t = Tarea.query.get_or_404(id)
    return jsonify({
        "id": t.id,
        "materia_id": t.materia_id,
        "materia_nombre": t.materia.nombre if t.materia else None,
        "profesor_id": t.profesor_id,
        "profesor_nombre": t.profesor.nombre_completo if t.profesor else None,
        "titulo": t.titulo,
        "descripcion": t.descripcion,
        "fecha_entrega": t.fecha_entrega.isoformat() if t.fecha_entrega else None
    })

def crear_tarea(request):
    data = request.get_json()
    nueva = Tarea(
        materia_id=data.get('materia_id'),
        profesor_id=data.get('profesor_id'),
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        fecha_entrega=data.get('fecha_entrega')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Tarea creada con éxito"}), 201

def actualizar_tarea(id, request):
    t = Tarea.query.get_or_404(id)
    data = request.get_json()

    t.materia_id = data.get('materia_id', t.materia_id)
    t.profesor_id = data.get('profesor_id', t.profesor_id)
    t.titulo = data.get('titulo', t.titulo)
    t.descripcion = data.get('descripcion', t.descripcion)
    t.fecha_entrega = data.get('fecha_entrega', t.fecha_entrega)

    db.session.commit()
    return jsonify({"mensaje": "Tarea actualizada con éxito"})

def eliminar_tarea(id):
    t = Tarea.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"mensaje": "Tarea eliminada con éxito"})
