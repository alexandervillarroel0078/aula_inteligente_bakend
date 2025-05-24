from flask import jsonify
from models import db
from models.periodo import Periodo
from traits.bitacora_trait import registrar_bitacora

def listar_periodos():
    periodos = Periodo.query.all()
    return jsonify([
        {
            "id": p.id,
            "nombre": p.nombre,
            "fecha_inicio": p.fecha_inicio,
            "fecha_fin": p.fecha_fin,
            "estado": p.estado,
            "semestre": p.semestre,
            "anio": p.anio
        } for p in periodos
    ])

def ver_periodo(id):
    p = Periodo.query.get_or_404(id)
    return jsonify({
        "id": p.id,
        "nombre": p.nombre,
        "fecha_inicio": p.fecha_inicio,
        "fecha_fin": p.fecha_fin,
        "estado": p.estado,
        "semestre": p.semestre,
        "anio": p.anio
    })

def crear_periodo(request):
    data = request.get_json()
    nuevo = Periodo(
        nombre = data['nombre'],
        fecha_inicio = data['fecha_inicio'],
        fecha_fin = data['fecha_fin'],
        estado = data['estado'],
        semestre = data['semestre'],
        anio = data['anio']
    )
    db.session.add(nuevo)
    db.session.commit()
    registrar_bitacora("periodo", f"creó periodo ID {nuevo.id}")
    return jsonify({"mensaje": "Periodo creado correctamente", "id": nuevo.id})

def editar_periodo(id, request):
    p = Periodo.query.get_or_404(id)
    data = request.get_json()

    p.nombre = data['nombre']
    p.fecha_inicio = data['fecha_inicio']
    p.fecha_fin = data['fecha_fin']
    p.estado = data['estado']
    p.semestre = data['semestre']
    p.anio = data['anio']

    db.session.commit()
    registrar_bitacora("periodo", f"editó periodo ID {p.id}")
    return jsonify({"mensaje": "Periodo actualizado correctamente"})

def eliminar_periodo(id):
    p = Periodo.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    registrar_bitacora("periodo", f"eliminó periodo ID {id}")
    return jsonify({"mensaje": "Periodo eliminado correctamente"})
