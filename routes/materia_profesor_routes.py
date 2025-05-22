from flask import Blueprint, request
from controllers import materia_profesor_controller

materia_profesor_bp = Blueprint('materia_profesor_bp', __name__)

@materia_profesor_bp.route('/api/materia-profesor', methods=['GET'])
def listar_materia_profesor():
    return materia_profesor_controller.listar_materia_profesor()

@materia_profesor_bp.route('/api/materia-profesor/<int:id>', methods=['GET'])
def obtener_materia_profesor(id):
    return materia_profesor_controller.obtener_materia_profesor(id)

@materia_profesor_bp.route('/api/materia-profesor', methods=['POST'])
def crear_materia_profesor():
    return materia_profesor_controller.crear_materia_profesor(request)

@materia_profesor_bp.route('/api/materia-profesor/<int:id>', methods=['PUT'])
def actualizar_materia_profesor(id):
    return materia_profesor_controller.actualizar_materia_profesor(id, request)

@materia_profesor_bp.route('/api/materia-profesor/<int:id>', methods=['DELETE'])
def eliminar_materia_profesor(id):
    return materia_profesor_controller.eliminar_materia_profesor(id)
