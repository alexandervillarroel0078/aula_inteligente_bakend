from flask import Blueprint, request
from controllers import entrega_tarea_controller

entrega_tarea_bp = Blueprint('entrega_tarea_bp', __name__)

@entrega_tarea_bp.route('/api/entregas', methods=['GET'])
def listar_entregas_tarea():
    return entrega_tarea_controller.listar_entregas_tarea()

@entrega_tarea_bp.route('/api/entregas/<int:id>', methods=['GET'])
def obtener_entrega_tarea(id):
    return entrega_tarea_controller.obtener_entrega_tarea(id)

@entrega_tarea_bp.route('/api/entregas', methods=['POST'])
def crear_entrega_tarea():
    return entrega_tarea_controller.crear_entrega_tarea(request)

@entrega_tarea_bp.route('/api/entregas/<int:id>', methods=['PUT'])
def actualizar_entrega_tarea(id):
    return entrega_tarea_controller.actualizar_entrega_tarea(id, request)

@entrega_tarea_bp.route('/api/entregas/<int:id>', methods=['DELETE'])
def eliminar_entrega_tarea(id):
    return entrega_tarea_controller.eliminar_entrega_tarea(id)
