from flask import jsonify
from models import db
from models.periodo import Periodo

def listar_periodos():
    periodos = Periodo.query.all()
    return jsonify([
        {
            "id": p.id,
            "nombre": p.nombre,
            "fecha_inicio": p.fecha_inicio.isoformat() if p.fecha_inicio else None,
            "fecha_fin": p.fecha_fin.isoformat() if p.fecha_fin else None,
            "estado": p.estado
        } for p in periodos
    ])

def obtener_periodo(id):
    periodo = Periodo.query.get_or_404(id)
    return jsonify({
        "id": periodo.id,
        "nombre": periodo.nombre,
        "fecha_inicio": periodo.fecha_inicio.isoformat() if periodo.fecha_inicio else None,
        "fecha_fin": periodo.fecha_fin.isoformat() if periodo.fecha_fin else None,
        "estado": periodo.estado
    })

def crear_periodo(request):
    data = request.get_json()
    nuevo = Periodo(
        nombre=data.get('nombre'),
        fecha_inicio=data.get('fecha_inicio'),
        fecha_fin=data.get('fecha_fin'),
        estado=data.get('estado')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Periodo creado con éxito"}), 201

def actualizar_periodo(id, request):
    periodo = Periodo.query.get_or_404(id)
    data = request.get_json()

    periodo.nombre = data.get('nombre', periodo.nombre)
    periodo.fecha_inicio = data.get('fecha_inicio', periodo.fecha_inicio)
    periodo.fecha_fin = data.get('fecha_fin', periodo.fecha_fin)
    periodo.estado = data.get('estado', periodo.estado)

    db.session.commit()
    return jsonify({"mensaje": "Periodo actualizado con éxito"})

def eliminar_periodo(id):
    periodo = Periodo.query.get_or_404(id)
    db.session.delete(periodo)
    db.session.commit()
    return jsonify({"mensaje": "Periodo eliminado con éxito"})
