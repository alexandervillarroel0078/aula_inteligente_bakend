from flask import jsonify
from models.gestion import Gestion
from models.grado import Grado

def listar_gestiones():
    gestiones = Gestion.query.order_by(Gestion.anio.desc()).all()
    resultado = [
        {
            "id": g.id,
            "anio": g.anio,
            "descripcion": g.descripcion,
            "estado": g.estado
        }
        for g in gestiones
    ]
    return jsonify(resultado), 200  # 👈 Este return estaba mal indentado

