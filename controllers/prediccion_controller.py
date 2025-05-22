from flask import jsonify
from models import db
from models.prediccion import Prediccion

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
        } for p in predicciones
    ])

def obtener_prediccion(id):
    p = Prediccion.query.get_or_404(id)
    return jsonify({
        "id": p.id,
        "alumno_id": p.alumno_id,
        "alumno_nombre": p.alumno.nombre_completo if p.alumno else None,
        "periodo_id": p.periodo_id,
        "periodo_nombre": p.periodo.nombre if p.periodo else None,
        "promedio_notas": p.promedio_notas,
        "porcentaje_asistencia": p.porcentaje_asistencia,
        "promedio_participaciones": p.promedio_participaciones,
        "resultado_predicho": p.resultado_predicho
    })

def crear_prediccion(request):
    data = request.get_json()
    nueva = Prediccion(
        alumno_id=data.get('alumno_id'),
        periodo_id=data.get('periodo_id'),
        promedio_notas=data.get('promedio_notas'),
        porcentaje_asistencia=data.get('porcentaje_asistencia'),
        promedio_participaciones=data.get('promedio_participaciones'),
        resultado_predicho=data.get('resultado_predicho')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Predicción registrada con éxito"}), 201

def actualizar_prediccion(id, request):
    p = Prediccion.query.get_or_404(id)
    data = request.get_json()

    p.alumno_id = data.get('alumno_id', p.alumno_id)
    p.periodo_id = data.get('periodo_id', p.periodo_id)
    p.promedio_notas = data.get('promedio_notas', p.promedio_notas)
    p.porcentaje_asistencia = data.get('porcentaje_asistencia', p.porcentaje_asistencia)
    p.promedio_participaciones = data.get('promedio_participaciones', p.promedio_participaciones)
    p.resultado_predicho = data.get('resultado_predicho', p.resultado_predicho)

    db.session.commit()
    return jsonify({"mensaje": "Predicción actualizada con éxito"})

def eliminar_prediccion(id):
    p = Prediccion.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"mensaje": "Predicción eliminada con éxito"})
