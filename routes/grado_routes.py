# app/routes/grado_routes.py
from flask import Blueprint, jsonify
from models import db
from models.grado import Grado  # asegúrate que la importación sea correcta

grado_bp = Blueprint('grado_bp', __name__)

@grado_bp.route('/api/grados', methods=['GET'])
def listar_grados():
    grados = Grado.query.all()
    resultado = []
    for g in grados:
        resultado.append({
            "id": g.id,
            "nombre": g.nombre,
            "nivel": g.nivel,
            "turno": g.turno,
            "gestion": g.gestion,
            "ubicacion": g.ubicacion,
            "seccion": g.seccion,
            "paralelo": g.paralelo
        })
    return jsonify(resultado)
