from flask import jsonify, request
from models import db
from models import db, Grado, Materia
from sqlalchemy.orm import joinedload
from models.grado_materia import GradoMateria
from traits.bitacora_trait import registrar_bitacora

# Listar grados
def listar_grados():
    grados = Grado.query.all()
    resultado = [{
        "id": g.id,
        "nombre": g.nombre,
        "nivel": g.nivel,
        "seccion": g.seccion,
        "paralelo": g.paralelo,
        "turno": g.turno,
        "ubicacion": g.ubicacion,
        "codigoGrado": g.codigoGrado,
        "gestion_id": g.gestion_id,
        "gestion_anio": g.gestion.anio,       
    } for g in grados]
    return jsonify(resultado), 200

def obtener_materias_por_grado():
    grados = Grado.query.options(
        joinedload(Grado.gestion),
        joinedload(Grado.grado_materias).joinedload(GradoMateria.materia_base)
    ).all()

    resultado = []

    for grado in grados:
        materias = [gm.materia_base.nombre for gm in grado.grado_materias]
        resultado.append({
            'grado_id': grado.id,
            'nombre': grado.nombre,
            'gestion': grado.gestion.anio,
            'codigoGrado': grado.codigoGrado,
            'materias': materias
        })
