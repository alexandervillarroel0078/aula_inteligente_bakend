from flask import Blueprint, request
from controllers import alumno_controller
from controllers.alumno_controller import (
    obtener_perfil_estudiante,
    obtener_notas_estudiante,
    obtener_asistencias_estudiante,
    obtener_participaciones_estudiante,
    obtener_predicciones_estudiante,
    obtener_historial_estudiante,
    obtener_materias_estudiante
)

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

# Ruta: Perfil
@alumno_bp.route('/api/alumnos/<int:alumno_id>/perfil', methods=['GET'])
def perfil_estudiante(alumno_id):
    return obtener_perfil_estudiante(alumno_id)

# Ruta: Notas
@alumno_bp.route('/api/alumnos/<int:alumno_id>/notas', methods=['GET'])
def notas_estudiante(alumno_id):
    return obtener_notas_estudiante(alumno_id)

# Ruta: Asistencias
@alumno_bp.route('/api/alumnos/<int:alumno_id>/asistencias', methods=['GET'])
def asistencias_estudiante(alumno_id):
    return obtener_asistencias_estudiante(alumno_id)

# Ruta: Participaciones
@alumno_bp.route('/api/alumnos/<int:alumno_id>/participaciones', methods=['GET'])
def participaciones_estudiante(alumno_id):
    return obtener_participaciones_estudiante(alumno_id)

# Ruta: Predicciones
@alumno_bp.route('/api/alumnos/<int:alumno_id>/predicciones', methods=['GET'])
def predicciones_estudiante(alumno_id):
    return obtener_predicciones_estudiante(alumno_id)

# Ruta: Historial
@alumno_bp.route('/api/alumnos/<int:alumno_id>/historial', methods=['GET'])
def historial_estudiante(alumno_id):
    return obtener_historial_estudiante(alumno_id)

# Ruta: Materias
@alumno_bp.route('/api/alumnos/<int:alumno_id>/materias', methods=['GET'])
def materias_estudiante(alumno_id):
    return obtener_materias_estudiante(alumno_id)
