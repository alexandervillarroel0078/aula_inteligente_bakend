from flask import jsonify
from models import db
from models.asistencia import Asistencia

def listar_asistencias():
    asistencias = Asistencia.query.all()
    return jsonify([
        {
            "id": a.id,
            "alumno_id": a.alumno_id,
            "alumno_nombre": a.alumno.nombre_completo if a.alumno else None,
            "materia_id": a.materia_id,
            "materia_nombre": a.materia.nombre if a.materia else None,
            "periodo_id": a.periodo_id,
            "periodo_nombre": a.periodo.nombre if a.periodo else None,
            "fecha": a.fecha.isoformat() if a.fecha else None,
            "presente": a.presente
        } for a in asistencias
    ])

def obtener_asistencia(id):
    a = Asistencia.query.get_or_404(id)
    return jsonify({
        "id": a.id,
        "alumno_id": a.alumno_id,
        "alumno_nombre": a.alumno.nombre_completo if a.alumno else None,
        "materia_id": a.materia_id,
        "materia_nombre": a.materia.nombre if a.materia else None,
        "periodo_id": a.periodo_id,
        "periodo_nombre": a.periodo.nombre if a.periodo else None,
        "fecha": a.fecha.isoformat() if a.fecha else None,
        "presente": a.presente
    })

def crear_asistencia(request):
    data = request.get_json()
    nueva = Asistencia(
        alumno_id=data.get('alumno_id'),
        materia_id=data.get('materia_id'),
        periodo_id=data.get('periodo_id'),
        fecha=data.get('fecha'),
        presente=data.get('presente')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Asistencia registrada con éxito"}), 201

def actualizar_asistencia(id, request):
    a = Asistencia.query.get_or_404(id)
    data = request.get_json()

    a.alumno_id = data.get('alumno_id', a.alumno_id)
    a.materia_id = data.get('materia_id', a.materia_id)
    a.periodo_id = data.get('periodo_id', a.periodo_id)
    a.fecha = data.get('fecha', a.fecha)
    a.presente = data.get('presente', a.presente)

    db.session.commit()
    return jsonify({"mensaje": "Asistencia actualizada con éxito"})

def eliminar_asistencia(id):
    a = Asistencia.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    return jsonify({"mensaje": "Asistencia eliminada con éxito"})
