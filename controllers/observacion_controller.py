from flask import jsonify, request
from models import db
from models.observacion import Observacion
from traits.bitacora_trait import registrar_bitacora

def listar_observaciones():
    observaciones = Observacion.query.all()
    return jsonify([{
        "id": o.id,
        "alumno_id": o.alumno_id,
        "alumno_nombre": o.alumno.nombre_completo if o.alumno else None,
        "profesor_id": o.profesor_id,
        "profesor_nombre": o.profesor.nombre_completo if o.profesor else None,
        "periodo_id": o.periodo_id,
        "periodo_nombre": o.periodo.nombre if o.periodo else None,
        "fecha": o.fecha,
        "descripcion": o.descripcion
    } for o in observaciones])

def ver_observacion(id):
    o = Observacion.query.get_or_404(id)
    return jsonify({
        "id": o.id,
        "alumno_id": o.alumno_id,
        "profesor_id": o.profesor_id,
        "periodo_id": o.periodo_id,
        "fecha": o.fecha,
        "descripcion": o.descripcion
    })

def crear_observacion(request):
    data = request.get_json()
    nueva = Observacion(
        alumno_id = data['alumno_id'],
        profesor_id = data['profesor_id'],
        periodo_id = data['periodo_id'],
        fecha = data['fecha'],
        descripcion = data['descripcion']
    )
    db.session.add(nueva)
    db.session.commit()
    registrar_bitacora("observacion", f"creó observación ID {nueva.id}")
    return jsonify({"mensaje": "Observación registrada correctamente", "id": nueva.id})

def editar_observacion(id, request):
    o = Observacion.query.get_or_404(id)
    data = request.get_json()

    o.alumno_id = data['alumno_id']
    o.profesor_id = data['profesor_id']
    o.periodo_id = data['periodo_id']
    o.fecha = data['fecha']
    o.descripcion = data['descripcion']

    db.session.commit()
    registrar_bitacora("observacion", f"editó observación ID {id}")
    return jsonify({"mensaje": "Observación actualizada correctamente"})

def eliminar_observacion(id):
    o = Observacion.query.get_or_404(id)
    db.session.delete(o)
    db.session.commit()
    registrar_bitacora("observacion", f"eliminó observación ID {id}")
    return jsonify({"mensaje": "Observación eliminada correctamente"})
