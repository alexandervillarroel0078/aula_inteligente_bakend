from flask import jsonify
from models import db
from models.nota import Nota

def listar_notas():
    notas = Nota.query.all()
    return jsonify([
        {
            "id": n.id,
            "alumno_id": n.alumno_id,
            "alumno_nombre": n.alumno.nombre_completo if n.alumno else None,
            "materia_id": n.materia_id,
            "materia_nombre": n.materia.nombre if n.materia else None,
            "periodo_id": n.periodo_id,
            "periodo_nombre": n.periodo.nombre if n.periodo else None,
            "nota_final": n.nota_final,
            "observaciones": n.observaciones
        } for n in notas
    ])

def obtener_nota(id):
    n = Nota.query.get_or_404(id)
    return jsonify({
        "id": n.id,
        "alumno_id": n.alumno_id,
        "alumno_nombre": n.alumno.nombre_completo if n.alumno else None,
        "materia_id": n.materia_id,
        "materia_nombre": n.materia.nombre if n.materia else None,
        "periodo_id": n.periodo_id,
        "periodo_nombre": n.periodo.nombre if n.periodo else None,
        "nota_final": n.nota_final,
        "observaciones": n.observaciones
    })

def crear_nota(request):
    data = request.get_json()
    nueva = Nota(
        alumno_id=data.get('alumno_id'),
        materia_id=data.get('materia_id'),
        periodo_id=data.get('periodo_id'),
        nota_final=data.get('nota_final'),
        observaciones=data.get('observaciones')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Nota registrada con éxito"}), 201

def actualizar_nota(id, request):
    nota = Nota.query.get_or_404(id)
    data = request.get_json()

    nota.alumno_id = data.get('alumno_id', nota.alumno_id)
    nota.materia_id = data.get('materia_id', nota.materia_id)
    nota.periodo_id = data.get('periodo_id', nota.periodo_id)
    nota.nota_final = data.get('nota_final', nota.nota_final)
    nota.observaciones = data.get('observaciones', nota.observaciones)

    db.session.commit()
    return jsonify({"mensaje": "Nota actualizada con éxito"})

def eliminar_nota(id):
    nota = Nota.query.get_or_404(id)
    db.session.delete(nota)
    db.session.commit()
    return jsonify({"mensaje": "Nota eliminada con éxito"})
