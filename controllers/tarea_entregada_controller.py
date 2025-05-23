from flask import jsonify
from models import db
from models.tarea_entregada import TareaEntregada  # antes EntregaTarea
from traits.bitacora_trait import registrar_bitacora

# GET - Listar todas las tareas entregadas
def listar_tareas_entregadas():
    tareas = TareaEntregada.query.all()
    return jsonify([
        {
            "id": t.id,
            "tarea_id": t.tarea_id,
            "tarea_titulo": t.tarea.titulo if t.tarea else None,
            "alumno_id": t.alumno_id,
            "alumno_nombre": t.alumno.nombre_completo if t.alumno else None,
            "archivo_url": t.archivo_url,
            "fecha_entrega": t.fecha_entrega.isoformat() if t.fecha_entrega else None,
            "calificacion": t.calificacion
        } for t in tareas
    ])

# GET - Ver una tarea entregada específica
def obtener_tarea_entregada(id):
    t = TareaEntregada.query.get_or_404(id)
    return jsonify({
        "id": t.id,
        "tarea_id": t.tarea_id,
        "tarea_titulo": t.tarea.titulo if t.tarea else None,
        "alumno_id": t.alumno_id,
        "alumno_nombre": t.alumno.nombre_completo if t.alumno else None,
        "archivo_url": t.archivo_url,
        "fecha_entrega": t.fecha_entrega.isoformat() if t.fecha_entrega else None,
        "calificacion": t.calificacion
    })

# POST - Crear nueva tarea entregada
def crear_tarea_entregada(request):
    data = request.get_json()
    nueva = TareaEntregada(
        tarea_id=data.get('tarea_id'),
        alumno_id=data.get('alumno_id'),
        archivo_url=data.get('archivo_url'),
        fecha_entrega=data.get('fecha_entrega'),
        calificacion=data.get('calificacion')
    )
    db.session.add(nueva)
    db.session.commit()
    registrar_bitacora("tarea_entregada", f"creó tarea entregada ID {nueva.id}")
    return jsonify({"mensaje": "Tarea entregada registrada con éxito", "id": nueva.id}), 201

# PUT - Actualizar tarea entregada
def actualizar_tarea_entregada(id, request):
    t = TareaEntregada.query.get_or_404(id)
    data = request.get_json()

    t.tarea_id = data.get('tarea_id', t.tarea_id)
    t.alumno_id = data.get('alumno_id', t.alumno_id)
    t.archivo_url = data.get('archivo_url', t.archivo_url)
    t.fecha_entrega = data.get('fecha_entrega', t.fecha_entrega)
    t.calificacion = data.get('calificacion', t.calificacion)

    db.session.commit()
    registrar_bitacora("tarea_entregada", f"editó tarea entregada ID {t.id}")
    return jsonify({"mensaje": "Tarea entregada actualizada con éxito"})

# DELETE - Eliminar tarea entregada
def eliminar_tarea_entregada(id):
    t = TareaEntregada.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    registrar_bitacora("tarea_entregada", f"eliminó tarea entregada ID {id}")
    return jsonify({"mensaje": "Tarea entregada eliminada con éxito"})
