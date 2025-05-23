from flask import jsonify, request
from models import db
from models.nota import Nota
from traits.bitacora_trait import registrar_bitacora

def listar_notas():
    notas = Nota.query.all()
    return jsonify([
        {
            "id": n.id,
            "nota_final": n.nota_final,
            "observaciones": n.observaciones,
            "alumno": {
                "id": n.alumno.id,
                "nombre_completo": n.alumno.nombre_completo
            } if n.alumno else None,
            "materia": {
                "id": n.materia.id,
                "nombre": n.materia.nombre
            } if n.materia else None,
            "periodo": {
                "id": n.periodo.id,
                "nombre": n.periodo.nombre
            } if n.periodo else None
        }
        for n in notas
    ])

def ver_nota(id):
    n = Nota.query.get_or_404(id)
    return jsonify({
        "id": n.id,
        "alumno_id": n.alumno_id,
        "materia_id": n.materia_id,
        "periodo_id": n.periodo_id,
        "nota_final": n.nota_final,
        "observaciones": n.observaciones
    })

def crear_nota(request):
    data = request.get_json()
    nueva = Nota(
        alumno_id=data['alumno_id'],
        materia_id=data['materia_id'],
        periodo_id=data['periodo_id'],
        nota_final=data['nota_final'],
        observaciones=data.get('observaciones')
    )
    db.session.add(nueva)
    db.session.commit()
    registrar_bitacora("nota", f"creó nota ID {nueva.id}")
    return jsonify({"mensaje": "Nota registrada correctamente", "id": nueva.id})

def editar_nota(id, request):
    n = Nota.query.get_or_404(id)
    data = request.get_json()

    n.alumno_id = data['alumno_id']
    n.materia_id = data['materia_id']
    n.periodo_id = data['periodo_id']
    n.nota_final = data['nota_final']
    n.observaciones = data.get('observaciones')

    db.session.commit()
    registrar_bitacora("nota", f"editó nota ID {id}")
    return jsonify({"mensaje": "Nota actualizada correctamente"})

def eliminar_nota(id):
    n = Nota.query.get_or_404(id)
    db.session.delete(n)
    db.session.commit()
    registrar_bitacora("nota", f"eliminó nota ID {id}")
    return jsonify({"mensaje": "Nota eliminada correctamente"})

def obtener_notas_por_alumno_controller(alumno_id):
    notas = Nota.query.filter_by(alumno_id=alumno_id).all()
    resultado = []
    for n in notas:
        resultado.append({
            "id": n.id,
            "alumno_id": n.alumno_id,
            "materia_id": n.materia_id,
            "materia_nombre": n.materia.nombre if n.materia else None,
            "periodo_id": n.periodo_id,
            "periodo_nombre": n.periodo.nombre if n.periodo else None,
            "nota_final": n.nota_final,
            "observaciones": n.observaciones
        })
    return jsonify(resultado)