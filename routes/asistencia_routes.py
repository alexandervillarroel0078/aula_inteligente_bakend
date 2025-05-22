from flask import Blueprint, request
from controllers import asistencia_controller

asistencia_bp = Blueprint('asistencia_bp', __name__)

@asistencia_bp.route('/api/asistencias', methods=['GET'])
def listar_asistencias():
    return asistencia_controller.listar_asistencias()

@asistencia_bp.route('/api/asistencias/<int:id>', methods=['GET'])
def obtener_asistencia(id):
    return asistencia_controller.obtener_asistencia(id)

@asistencia_bp.route('/api/asistencias', methods=['POST'])
def crear_asistencia():
    return asistencia_controller.crear_asistencia(request)

@asistencia_bp.route('/api/asistencias/<int:id>', methods=['PUT'])
def actualizar_asistencia(id):
    return asistencia_controller.actualizar_asistencia(id, request)

@asistencia_bp.route('/api/asistencias/<int:id>', methods=['DELETE'])
def eliminar_asistencia(id):
    return asistencia_controller.eliminar_asistencia(id)
