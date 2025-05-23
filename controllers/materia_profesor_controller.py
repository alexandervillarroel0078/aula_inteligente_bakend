from flask import jsonify, request
from models import db
from models.materia_profesor import MateriaProfesor
from traits.bitacora_trait import registrar_bitacora

# Obtener todas las materias asignadas a profesores
def listar_materias_profesor():
    registros = MateriaProfesor.query.all()
    return jsonify([
        {
            "id": mp.id,
            "materia_id": mp.materia_id,
            "materia_nombre": mp.materia.nombre if mp.materia else None,
            "profesor_id": mp.profesor_id,
            "profesor_nombre": mp.profesor.nombre_completo if mp.profesor else None,
            "fecha_asignacion": mp.fecha_asignacion.isoformat() if mp.fecha_asignacion else None
        }
        for mp in registros
    ])


# Ver una asignación específica
def ver_materia_profesor(id):
    mp = MateriaProfesor.query.get_or_404(id)
    return jsonify({
        "id": mp.id,
        "materia_id": mp.materia_id,
        "profesor_id": mp.profesor_id,
        "fecha_asignacion": mp.fecha_asignacion.isoformat() if mp.fecha_asignacion else None
    })

# Crear nueva asignación
def crear_materia_profesor(request):
    data = request.get_json()
    nueva = MateriaProfesor(
        materia_id=data['materia_id'],
        profesor_id=data['profesor_id'],
        fecha_asignacion=data.get('fecha_asignacion')
    )
    db.session.add(nueva)
    db.session.commit()
    registrar_bitacora("materia_profesor", f"creó asignación ID {nueva.id}")
    return jsonify({"mensaje": "Materia asignada al profesor correctamente", "id": nueva.id})

# Editar asignación
def editar_materia_profesor(id, request):
    mp = MateriaProfesor.query.get_or_404(id)
    data = request.get_json()
    mp.materia_id = data['materia_id']
    mp.profesor_id = data['profesor_id']
    mp.fecha_asignacion = data.get('fecha_asignacion')
    db.session.commit()
    registrar_bitacora("materia_profesor", f"editó asignación ID {id}")
    return jsonify({"mensaje": "Asignación actualizada correctamente"})

# Eliminar asignación
def eliminar_materia_profesor(id):
    mp = MateriaProfesor.query.get_or_404(id)
    db.session.delete(mp)
    db.session.commit()
    registrar_bitacora("materia_profesor", f"eliminó asignación ID {id}")
    return jsonify({"mensaje": "Asignación eliminada correctamente"})
