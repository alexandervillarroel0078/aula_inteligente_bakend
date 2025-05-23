from flask import Blueprint, request
from controllers import usuario_controller

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    return usuario_controller.listar_usuarios()

@usuario_bp.route('/api/usuarios/<int:id>', methods=['GET'])
def ver_usuario(id):
    return usuario_controller.ver_usuario(id)

@usuario_bp.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    return usuario_controller.crear_usuario(request)

@usuario_bp.route('/api/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    return usuario_controller.editar_usuario(id, request)

@usuario_bp.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    return usuario_controller.eliminar_usuario(id)
