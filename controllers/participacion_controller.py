from flask import jsonify
from models import db
from models.participacion import Participacion
from traits.bitacora_trait import registrar_bitacora

def listar_participaciones():
    participaciones = Participacion.query.all()
    return jsonify([
        {
            "id": p.id,
            "alumno_id": p.alumno_id,
            "alumno_nombre": p.alumno.nombre_completo if p.alumno else None,
            "materia_id": p.materia_id,
            "materia_nombre": p.materia.nombre if p.materia else None,
            "periodo_id": p.periodo_id,
            "periodo_nombre": p.periodo.nombre if p.periodo else None,
            "fecha": p.fecha,
            "puntaje": p.puntaje
        } for p in participaciones
    ])

def ver_participacion(id):
    p = Participacion.query.get_or_404(id)
    return jsonify({
        "id": p.id,
        "alumno_id": p.alumno_id,
        "materia_id": p.materia_id,
        "periodo_id": p.periodo_id,
        "fecha": p.fecha,
        "puntaje": p.puntaje
    })

def crear_participacion(request):
    data = request.get_json()
    nueva = Participacion(
        alumno_id = data['alumno_id'],
        materia_id = data['materia_id'],
        periodo_id = data['periodo_id'],
        fecha = data['fecha'],
        puntaje = data['puntaje']
    )
    db.session.add(nueva)
    db.session.commit()
    registrar_bitacora("participacion", f"creó participación ID {nueva.id}")
    return jsonify({"mensaje": "Participación registrada correctamente", "id": nueva.id})

def editar_participacion(id, request):
    p = Participacion.query.get_or_404(id)
    data = request.get_json()

    p.alumno_id = data['alumno_id']
    p.materia_id = data['materia_id']
    p.periodo_id = data['periodo_id']
    p.fecha = data['fecha']
    p.puntaje = data['puntaje']

    db.session.commit()
    registrar_bitacora("participacion", f"editó participación ID {p.id}")
    return jsonify({"mensaje": "Participación actualizada correctamente"})

def eliminar_participacion(id):
    p = Participacion.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    registrar_bitacora("participacion", f"eliminó participación ID {id}")
    return jsonify({"mensaje": "Participación eliminada correctamente"})
