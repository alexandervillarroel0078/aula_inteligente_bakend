from flask import jsonify, request
from models import db
from models.materia import Materia
from traits.bitacora_trait import registrar_bitacora

def listar_materias():
    materias = Materia.query.all()
    return jsonify([{
        "id": m.id,
        "codigo": m.codigo,
        "nombre": m.nombre,
        "descripcion": m.descripcion,
        "turno": m.turno,
        "aula": m.aula,
        "estado": m.estado,
        'grado': {
    'id': m.grado.id if m.grado else None,
    'nombre': m.grado.nombre if m.grado else '-'
}

    } for m in materias])

def ver_materia(id):
    m = Materia.query.get_or_404(id)
    return jsonify({
        "id": m.id,
        "codigo": m.codigo,
        "nombre": m.nombre,
        "descripcion": m.descripcion,
        "turno": m.turno,
        "aula": m.aula,
        "estado": m.estado,
        "grado_id": m.grado_id
    })

def crear_materia(request):
    data = request.get_json()
    nueva = Materia(
        codigo=data['codigo'],
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        turno=data['turno'],
        aula=data['aula'],
        estado=data['estado'],
        grado_id=data['grado_id']
    )
    db.session.add(nueva)
    db.session.commit()
    registrar_bitacora("materia", f"creó materia ID {nueva.id}")
    return jsonify({"mensaje": "Materia registrada correctamente", "id": nueva.id})

def editar_materia(id, request):
    m = Materia.query.get_or_404(id)
    data = request.get_json()
    m.codigo = data['codigo']
    m.nombre = data['nombre']
    m.descripcion = data.get('descripcion')
    m.turno = data['turno']
    m.aula = data['aula']
    m.estado = data['estado']
    m.grado_id = data['grado_id']

    db.session.commit()
    registrar_bitacora("materia", f"editó materia ID {id}")
    return jsonify({"mensaje": "Materia actualizada correctamente"})

def eliminar_materia(id):
    m = Materia.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    registrar_bitacora("materia", f"eliminó materia ID {id}")
    return jsonify({"mensaje": "Materia eliminada correctamente"})
