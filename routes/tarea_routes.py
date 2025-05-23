from flask import Blueprint, request
from controllers import tarea_controller

tarea_bp = Blueprint('tarea_bp', __name__)

@tarea_bp.route('/api/tareas', methods=['GET'])
def listar_tareas():
    return tarea_controller.listar_tareas()

@tarea_bp.route('/api/tareas/<int:id>', methods=['GET'])
def ver_tarea(id):
    return tarea_controller.ver_tarea(id)

@tarea_bp.route('/api/tareas', methods=['POST'])
def crear_tarea():
    return tarea_controller.crear_tarea(request)

@tarea_bp.route('/api/tareas/<int:id>', methods=['PUT'])
def editar_tarea(id):
    return tarea_controller.editar_tarea(id, request)

@tarea_bp.route('/api/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    return tarea_controller.eliminar_tarea(id)
