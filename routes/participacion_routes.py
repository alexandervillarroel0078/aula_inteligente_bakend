from flask import Blueprint, request
from controllers import participacion_controller

participacion_bp = Blueprint('participacion_bp', __name__)

@participacion_bp.route('/api/participaciones', methods=['GET'])
def listar_participaciones():
    return participacion_controller.listar_participaciones()

@participacion_bp.route('/api/participaciones/<int:id>', methods=['GET'])
def ver_participacion(id):
    return participacion_controller.ver_participacion(id)

@participacion_bp.route('/api/participaciones', methods=['POST'])
def crear_participacion():
    return participacion_controller.crear_participacion(request)

@participacion_bp.route('/api/participaciones/<int:id>', methods=['PUT'])
def editar_participacion(id):
    return participacion_controller.editar_participacion(id, request)

@participacion_bp.route('/api/participaciones/<int:id>', methods=['DELETE'])
def eliminar_participacion(id):
    return participacion_controller.eliminar_participacion(id)
