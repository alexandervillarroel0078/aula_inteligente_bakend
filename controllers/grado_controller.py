from flask import jsonify, request
from models import db
from models.grado import Grado
from traits.bitacora_trait import registrar_bitacora

# Listar grados
def listar_grados():
    grados = Grado.query.all()
    return jsonify([{
        "id": g.id,
        "nombre": g.nombre,
        "nivel": g.nivel,
        "seccion": g.seccion,
        "paralelo": g.paralelo,
        "turno": g.turno,
        "gestion": g.gestion,
        "ubicacion": g.ubicacion
    } for g in grados])

# Ver grado
def ver_grado(id):
    g = Grado.query.get_or_404(id)
    return jsonify({
        "id": g.id,
        "nombre": g.nombre,
        "nivel": g.nivel,
        "seccion": g.seccion,
        "paralelo": g.paralelo,
        "turno": g.turno,
        "gestion": g.gestion,
        "ubicacion": g.ubicacion
    })

# Crear grado
def crear_grado(request):
    data = request.get_json()
    nuevo = Grado(
        nombre=data["nombre"],
        nivel=data["nivel"],
        seccion=data.get("seccion"),
        paralelo=data.get("paralelo"),
        turno=data["turno"],
        gestion=data["gestion"],
        ubicacion=data.get("ubicacion")
    )
    db.session.add(nuevo)
    db.session.commit()
    registrar_bitacora("grado", f"creó grado ID {nuevo.id}")
    return jsonify({"mensaje": "Grado creado correctamente", "id": nuevo.id})

# Editar grado
def editar_grado(id, request):
    g = Grado.query.get_or_404(id)
    data = request.get_json()
    g.nombre = data["nombre"]
    g.nivel = data["nivel"]
    g.seccion = data.get("seccion")
    g.paralelo = data.get("paralelo")
    g.turno = data["turno"]
    g.gestion = data["gestion"]
    g.ubicacion = data.get("ubicacion")
    db.session.commit()
    registrar_bitacora("grado", f"editó grado ID {id}")
    return jsonify({"mensaje": "Grado actualizado correctamente"})

# Eliminar grado
def eliminar_grado(id):
    g = Grado.query.get_or_404(id)
    db.session.delete(g)
    db.session.commit()
    registrar_bitacora("grado", f"eliminó grado ID {id}")
    return jsonify({"mensaje": "Grado eliminado correctamente"})
