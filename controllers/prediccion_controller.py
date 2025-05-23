from flask import jsonify
from models import db
from models.prediccion import Prediccion
from traits.bitacora_trait import registrar_bitacora

def listar_predicciones():
    predicciones = Prediccion.query.all()
    return jsonify([
        {
            "id": p.id,
            "alumno_id": p.alumno_id,
            "alumno_nombre": p.alumno.nombre_completo if p.alumno else None,
            "periodo_id": p.periodo_id,
            "periodo_nombre": p.periodo.nombre if p.periodo else None,
            "promedio_notas": p.promedio_notas,
            "porcentaje_asistencia": p.porcentaje_asistencia,
            "promedio_participaciones": p.promedio_participaciones,
            "resultado_predicho": p.resultado_predicho
        }
        for p in predicciones
    ])


def ver_prediccion(id):
    p = Prediccion.query.get_or_404(id)
    return jsonify({
        "id": p.id,
        "alumno_id": p.alumno_id,
        "periodo_id": p.periodo_id,
        "promedio_notas": p.promedio_notas,
        "porcentaje_asistencia": p.porcentaje_asistencia,
        "promedio_participaciones": p.promedio_participaciones,
        "resultado_predicho": p.resultado_predicho
    })

def crear_prediccion(request):
    data = request.get_json()
    nueva = Prediccion(
        alumno_id = data['alumno_id'],
        periodo_id = data['periodo_id'],
        promedio_notas = data['promedio_notas'],
        porcentaje_asistencia = data['porcentaje_asistencia'],
        promedio_participaciones = data['promedio_participaciones'],
        resultado_predicho = data['resultado_predicho']
    )
    db.session.add(nueva)
    db.session.commit()
    registrar_bitacora("prediccion", f"creó predicción ID {nueva.id}")
    return jsonify({"mensaje": "Predicción registrada correctamente", "id": nueva.id})

def editar_prediccion(id, request):
    p = Prediccion.query.get_or_404(id)
    data = request.get_json()

    p.alumno_id = data['alumno_id']
    p.periodo_id = data['periodo_id']
    p.promedio_notas = data['promedio_notas']
    p.porcentaje_asistencia = data['porcentaje_asistencia']
    p.promedio_participaciones = data['promedio_participaciones']
    p.resultado_predicho = data['resultado_predicho']

    db.session.commit()
    registrar_bitacora("prediccion", f"editó predicción ID {p.id}")
    return jsonify({"mensaje": "Predicción actualizada correctamente"})

def eliminar_prediccion(id):
    p = Prediccion.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    registrar_bitacora("prediccion", f"eliminó predicción ID {id}")
    return jsonify({"mensaje": "Predicción eliminada correctamente"})
