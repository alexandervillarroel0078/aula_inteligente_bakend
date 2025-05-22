from flask import jsonify
from models import db
from models.materia_profesor import MateriaProfesor

def listar_materia_profesor():
    registros = MateriaProfesor.query.all()
    return jsonify([
        {
            "id": mp.id,
            "materia_id": mp.materia_id,
            "materia_nombre": mp.materia.nombre if mp.materia else None,
            "profesor_id": mp.profesor_id,
            "profesor_nombre": mp.profesor.nombre_completo if mp.profesor else None,
            "fecha_asignacion": mp.fecha_asignacion.isoformat() if mp.fecha_asignacion else None
        } for mp in registros
    ])

def obtener_materia_profesor(id):
    mp = MateriaProfesor.query.get_or_404(id)
    return jsonify({
        "id": mp.id,
        "materia_id": mp.materia_id,
        "materia_nombre": mp.materia.nombre if mp.materia else None,
        "profesor_id": mp.profesor_id,
        "profesor_nombre": mp.profesor.nombre_completo if mp.profesor else None,
        "fecha_asignacion": mp.fecha_asignacion.isoformat() if mp.fecha_asignacion else None
    })

def crear_materia_profesor(request):
    data = request.get_json()
    nuevo = MateriaProfesor(
        materia_id=data.get('materia_id'),
        profesor_id=data.get('profesor_id'),
        fecha_asignacion=data.get('fecha_asignacion')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Asignación creada con éxito"}), 201

def actualizar_materia_profesor(id, request):
    mp = MateriaProfesor.query.get_or_404(id)
    data = request.get_json()

    mp.materia_id = data.get('materia_id', mp.materia_id)
    mp.profesor_id = data.get('profesor_id', mp.profesor_id)
    mp.fecha_asignacion = data.get('fecha_asignacion', mp.fecha_asignacion)

    db.session.commit()
    return jsonify({"mensaje": "Asignación actualizada con éxito"})

def eliminar_materia_profesor(id):
    mp = MateriaProfesor.query.get_or_404(id)
    db.session.delete(mp)
    db.session.commit()
    return jsonify({"mensaje": "Asignación eliminada con éxito"})
