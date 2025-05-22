from flask import Blueprint, request
from controllers import profesor_controller

profesor_bp = Blueprint('profesor_bp', __name__)

@profesor_bp.route('/api/profesores', methods=['GET'])
def listar_profesores():
    return profesor_controller.listar_profesores()

@profesor_bp.route('/api/profesores/<int:id>', methods=['GET'])
def obtener_profesor(id):
    return profesor_controller.obtener_profesor(id)

@profesor_bp.route('/api/profesores', methods=['POST'])
def crear_profesor():
    return profesor_controller.crear_profesor(request)

@profesor_bp.route('/api/profesores/<int:id>', methods=['PUT'])
def actualizar_profesor(id):
    return profesor_controller.actualizar_profesor(id, request)

@profesor_bp.route('/api/profesores/<int:id>', methods=['DELETE'])
def eliminar_profesor(id):
    return profesor_controller.eliminar_profesor(id)
