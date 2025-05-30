from flask import Blueprint, request
from controllers import grado_controller

grado_bp = Blueprint('grado_bp', __name__)

#http://127.0.0.1:5000/api/grados
@grado_bp.route('/api/grados', methods=['GET'])
def listar_grados():
    return grado_controller.listar_grados()

#http://127.0.0.1:5000/api/grado/materias?grado_id=3
@grado_bp.route('/api/grado/materias', methods=['GET'])
def obtener_materias_por_grado():
    return grado_controller.obtener_materias_por_grado()