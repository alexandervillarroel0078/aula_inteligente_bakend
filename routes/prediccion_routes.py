from flask import Blueprint, request
from controllers import prediccion_controller

prediccion_bp = Blueprint('prediccion_bp', __name__)

@prediccion_bp.route('/api/predicciones', methods=['GET'])
def listar_predicciones():
    return prediccion_controller.listar_predicciones()

@prediccion_bp.route('/api/predicciones/<int:id>', methods=['GET'])
def ver_prediccion(id):
    return prediccion_controller.ver_prediccion(id)

@prediccion_bp.route('/api/predicciones', methods=['POST'])
def crear_prediccion():
    return prediccion_controller.crear_prediccion(request)

@prediccion_bp.route('/api/predicciones/<int:id>', methods=['PUT'])
def editar_prediccion(id):
    return prediccion_controller.editar_prediccion(id, request)

@prediccion_bp.route('/api/predicciones/<int:id>', methods=['DELETE'])
def eliminar_prediccion(id):
    return prediccion_controller.eliminar_prediccion(id)
