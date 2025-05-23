from flask import Blueprint, request
from controllers import nota_controller

nota_bp = Blueprint('nota_bp', __name__)

@nota_bp.route('/api/notas', methods=['GET'])
def listar_notas():
    return nota_controller.listar_notas()

@nota_bp.route('/api/notas/<int:id>', methods=['GET'])
def ver_nota(id):
    return nota_controller.ver_nota(id)

@nota_bp.route('/api/notas', methods=['POST'])
def crear_nota():
    return nota_controller.crear_nota(request)

@nota_bp.route('/api/notas/<int:id>', methods=['PUT'])
def editar_nota(id):
    return nota_controller.editar_nota(id, request)

@nota_bp.route('/api/notas/<int:id>', methods=['DELETE'])
def eliminar_nota(id):
    return nota_controller.eliminar_nota(id)
