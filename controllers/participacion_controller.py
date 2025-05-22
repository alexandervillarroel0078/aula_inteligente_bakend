from flask import jsonify
from models import db
from models.participacion import Participacion

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
            "fecha": p.fecha.isoformat() if p.fecha else None,
            "puntaje": p.puntaje
        } for p in participaciones
    ])

def obtener_participacion(id):
    p = Participacion.query.get_or_404(id)
    return jsonify({
        "id": p.id,
        "alumno_id": p.alumno_id,
        "alumno_nombre": p.alumno.nombre_completo if p.alumno else None,
        "materia_id": p.materia_id,
        "materia_nombre": p.materia.nombre if p.materia else None,
        "periodo_id": p.periodo_id,
        "periodo_nombre": p.periodo.nombre if p.periodo else None,
        "fecha": p.fecha.isoformat() if p.fecha else None,
        "puntaje": p.puntaje
    })

def crear_participacion(request):
    data = request.get_json()
    nueva = Participacion(
        alumno_id=data.get('alumno_id'),
        materia_id=data.get('materia_id'),
        periodo_id=data.get('periodo_id'),
        fecha=data.get('fecha'),
        puntaje=data.get('puntaje')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Participación registrada con éxito"}), 201

def actualizar_participacion(id, request):
    p = Participacion.query.get_or_404(id)
    data = request.get_json()

    p.alumno_id = data.get('alumno_id', p.alumno_id)
    p.materia_id = data.get('materia_id', p.materia_id)
    p.periodo_id = data.get('periodo_id', p.periodo_id)
    p.fecha = data.get('fecha', p.fecha)
    p.puntaje = data.get('puntaje', p.puntaje)

    db.session.commit()
    return jsonify({"mensaje": "Participación actualizada con éxito"})

def eliminar_participacion(id):
    p = Participacion.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"mensaje": "Participación eliminada con éxito"})
