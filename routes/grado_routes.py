from flask import Blueprint, request
from controllers import grado_controller

grado_bp = Blueprint('grado_bp', __name__)

@grado_bp.route('/api/grados', methods=['GET'])
def listar_grados():
    return grado_controller.listar_grados()

@grado_bp.route('/api/grados/<int:id>', methods=['GET'])
def ver_grado(id):
    return grado_controller.ver_grado(id)

@grado_bp.route('/api/grados', methods=['POST'])
def crear_grado():
    return grado_controller.crear_grado(request)

@grado_bp.route('/api/grados/<int:id>', methods=['PUT'])
def editar_grado(id):
    return grado_controller.editar_grado(id, request)

@grado_bp.route('/api/grados/<int:id>', methods=['DELETE'])
def eliminar_grado(id):
    return grado_controller.eliminar_grado(id)
