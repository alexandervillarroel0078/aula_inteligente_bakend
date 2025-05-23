from flask import jsonify
from models import db
from models.asistencia import Asistencia
from traits.bitacora_trait import registrar_bitacora

# GET - Listar asistencias
def listar_asistencias():
    asistencias = Asistencia.query.all()
    data = []
    for a in asistencias:
        data.append({
            "id": a.id,
            "alumno_id": a.alumno_id,
            "materia_id": a.materia_id,
            "periodo_id": a.periodo_id,
            "fecha": a.fecha,
            "presente": a.presente
        })
    return jsonify(data)

# GET - Ver una asistencia
def ver_asistencia(id):
    a = Asistencia.query.get_or_404(id)
    return jsonify({
        "id": a.id,
        "alumno_id": a.alumno_id,
        "materia_id": a.materia_id,
        "periodo_id": a.periodo_id,
        "fecha": a.fecha,
        "presente": a.presente
    })

# POST - Crear nueva asistencia
def crear_asistencia(request):
    data = request.get_json()
    nueva = Asistencia(
        alumno_id = data['alumno_id'],
        materia_id = data['materia_id'],
        periodo_id = data['periodo_id'],
        fecha = data['fecha'],
        presente = data['presente']
    )
    db.session.add(nueva)
    db.session.commit()

    registrar_bitacora("asistencia", f"creó asistencia ID {nueva.id}")
    return jsonify({"message": "Asistencia registrada correctamente", "id": nueva.id})

# PUT - Editar asistencia
def editar_asistencia(id, request):
    a = Asistencia.query.get_or_404(id)
    data = request.get_json()

    a.alumno_id = data['alumno_id']
    a.materia_id = data['materia_id']
    a.periodo_id = data['periodo_id']
    a.fecha = data['fecha']
    a.presente = data['presente']

    db.session.commit()
    registrar_bitacora("asistencia", f"editó asistencia ID {a.id}")
    return jsonify({"message": "Asistencia actualizada correctamente"})

# DELETE - Eliminar asistencia
def eliminar_asistencia(id):
    a = Asistencia.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()

    registrar_bitacora("asistencia", f"eliminó asistencia ID {id}")
    return jsonify({"message": "Asistencia eliminada correctamente"})
