from flask import Blueprint, request
from controllers import rol_controller

rol_bp = Blueprint('rol_bp', __name__)

@rol_bp.route('/api/roles', methods=['GET'])
def listar_roles():
    return rol_controller.listar_roles()

@rol_bp.route('/api/roles/<int:id>', methods=['GET'])
def obtener_rol(id):
    return rol_controller.obtener_rol(id)

@rol_bp.route('/api/roles', methods=['POST'])
def crear_rol():
    return rol_controller.crear_rol(request)

@rol_bp.route('/api/roles/<int:id>', methods=['PUT'])
def actualizar_rol(id):
    return rol_controller.actualizar_rol(id, request)

@rol_bp.route('/api/roles/<int:id>', methods=['DELETE'])
def eliminar_rol(id):
    return rol_controller.eliminar_rol(id)
