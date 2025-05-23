from flask import Blueprint, request
from controllers import tarea_entregada_controller

tarea_entregada_bp = Blueprint('tarea_entregada_bp', __name__)

@tarea_entregada_bp.route('/api/tareas_entregadas', methods=['GET'])
def listar_tareas_entregadas():
    return tarea_entregada_controller.listar_tareas_entregadas()

@tarea_entregada_bp.route('/api/tareas_entregadas/<int:id>', methods=['GET'])
def obtener_tarea_entregada(id):
    return tarea_entregada_controller.obtener_tarea_entregada(id)

@tarea_entregada_bp.route('/api/tareas_entregadas', methods=['POST'])
def crear_tarea_entregada():
    return tarea_entregada_controller.crear_tarea_entregada(request)

@tarea_entregada_bp.route('/api/tareas_entregadas/<int:id>', methods=['PUT'])
def actualizar_tarea_entregada(id):
    return tarea_entregada_controller.actualizar_tarea_entregada(id, request)

@tarea_entregada_bp.route('/api/tareas_entregadas/<int:id>', methods=['DELETE'])
def eliminar_tarea_entregada(id):
    return tarea_entregada_controller.eliminar_tarea_entregada(id)
