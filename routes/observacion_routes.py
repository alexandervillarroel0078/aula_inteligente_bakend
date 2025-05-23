from flask import Blueprint, request
from controllers import observacion_controller

observacion_bp = Blueprint('observacion_bp', __name__)

@observacion_bp.route('/api/observaciones', methods=['GET'])
def listar_observaciones():
    return observacion_controller.listar_observaciones()

@observacion_bp.route('/api/observaciones/<int:id>', methods=['GET'])
def ver_observacion(id):
    return observacion_controller.ver_observacion(id)

@observacion_bp.route('/api/observaciones', methods=['POST'])
def crear_observacion():
    return observacion_controller.crear_observacion(request)

@observacion_bp.route('/api/observaciones/<int:id>', methods=['PUT'])
def editar_observacion(id):
    return observacion_controller.editar_observacion(id, request)

@observacion_bp.route('/api/observaciones/<int:id>', methods=['DELETE'])
def eliminar_observacion(id):
    return observacion_controller.eliminar_observacion(id)
