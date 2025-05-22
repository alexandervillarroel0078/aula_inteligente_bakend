from flask import Blueprint, request
from controllers import periodo_controller

periodo_bp = Blueprint('periodo_bp', __name__)

@periodo_bp.route('/api/periodos', methods=['GET'])
def listar_periodos():
    return periodo_controller.listar_periodos()

@periodo_bp.route('/api/periodos/<int:id>', methods=['GET'])
def obtener_periodo(id):
    return periodo_controller.obtener_periodo(id)

@periodo_bp.route('/api/periodos', methods=['POST'])
def crear_periodo():
    return periodo_controller.crear_periodo(request)

@periodo_bp.route('/api/periodos/<int:id>', methods=['PUT'])
def actualizar_periodo(id):
    return periodo_controller.actualizar_periodo(id, request)

@periodo_bp.route('/api/periodos/<int:id>', methods=['DELETE'])
def eliminar_periodo(id):
    return periodo_controller.eliminar_periodo(id)
