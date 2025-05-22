from flask import Blueprint, request
from controllers import materia_controller

materia_bp = Blueprint('materia_bp', __name__)

@materia_bp.route('/api/materias', methods=['GET'])
def listar_materias():
    return materia_controller.listar_materias()

@materia_bp.route('/api/materias/<int:id>', methods=['GET'])
def obtener_materia(id):
    return materia_controller.obtener_materia(id)

@materia_bp.route('/api/materias', methods=['POST'])
def crear_materia():
    return materia_controller.crear_materia(request)

@materia_bp.route('/api/materias/<int:id>', methods=['PUT'])
def actualizar_materia(id):
    return materia_controller.actualizar_materia(id, request)

@materia_bp.route('/api/materias/<int:id>', methods=['DELETE'])
def eliminar_materia(id):
    return materia_controller.eliminar_materia(id)
