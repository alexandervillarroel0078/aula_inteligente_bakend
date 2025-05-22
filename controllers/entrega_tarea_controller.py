from flask import jsonify
from models import db
from models.entrega_tarea import EntregaTarea

def listar_entregas_tarea():
    entregas = EntregaTarea.query.all()
    return jsonify([
        {
            "id": e.id,
            "tarea_id": e.tarea_id,
            "tarea_titulo": e.tarea.titulo if e.tarea else None,
            "alumno_id": e.alumno_id,
            "alumno_nombre": e.alumno.nombre_completo if e.alumno else None,
            "archivo_url": e.archivo_url,
            "fecha_entrega": e.fecha_entrega.isoformat() if e.fecha_entrega else None,
            "calificacion": e.calificacion
        } for e in entregas
    ])

def obtener_entrega_tarea(id):
    e = EntregaTarea.query.get_or_404(id)
    return jsonify({
        "id": e.id,
        "tarea_id": e.tarea_id,
        "tarea_titulo": e.tarea.titulo if e.tarea else None,
        "alumno_id": e.alumno_id,
        "alumno_nombre": e.alumno.nombre_completo if e.alumno else None,
        "archivo_url": e.archivo_url,
        "fecha_entrega": e.fecha_entrega.isoformat() if e.fecha_entrega else None,
        "calificacion": e.calificacion
    })

def crear_entrega_tarea(request):
    data = request.get_json()
    nueva = EntregaTarea(
        tarea_id=data.get('tarea_id'),
        alumno_id=data.get('alumno_id'),
        archivo_url=data.get('archivo_url'),
        fecha_entrega=data.get('fecha_entrega'),
        calificacion=data.get('calificacion')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Entrega de tarea registrada con éxito"}), 201

def actualizar_entrega_tarea(id, request):
    e = EntregaTarea.query.get_or_404(id)
    data = request.get_json()

    e.tarea_id = data.get('tarea_id', e.tarea_id)
    e.alumno_id = data.get('alumno_id', e.alumno_id)
    e.archivo_url = data.get('archivo_url', e.archivo_url)
    e.fecha_entrega = data.get('fecha_entrega', e.fecha_entrega)
    e.calificacion = data.get('calificacion', e.calificacion)

    db.session.commit()
    return jsonify({"mensaje": "Entrega de tarea actualizada con éxito"})

def eliminar_entrega_tarea(id):
    e = EntregaTarea.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return jsonify({"mensaje": "Entrega de tarea eliminada con éxito"})
