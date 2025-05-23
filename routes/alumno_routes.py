from flask import Blueprint, request
from controllers import alumno_controller

alumno_bp = Blueprint('alumno_bp', __name__)

@alumno_bp.route('/api/alumnos', methods=['GET'])
def listar_alumnos():
    return alumno_controller.listar_alumnos()

@alumno_bp.route('/api/alumnos/<int:id>', methods=['GET'])
def ver_alumno(id):
    return alumno_controller.ver_alumno(id)

@alumno_bp.route('/api/alumnos', methods=['POST'])
def crear_alumno():
    return alumno_controller.crear_alumno(request)

@alumno_bp.route('/api/alumnos/<int:id>', methods=['PUT'])
def editar_alumno(id):
    return alumno_controller.editar_alumno(id, request)

@alumno_bp.route('/api/alumnos/<int:id>', methods=['DELETE'])
def eliminar_alumno(id):
    return alumno_controller.eliminar_alumno(id)
