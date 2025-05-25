from flask import Blueprint, request
from controllers import profesor_controller
from controllers.profesor_controller import registrar_participaciones

profesor_bp = Blueprint('profesor_bp', __name__)

@profesor_bp.route('/api/profesores', methods=['GET'])
def listar_profesores():
    return profesor_controller.listar_profesores()

@profesor_bp.route('/api/profesores/<int:id>', methods=['GET'])
def obtener_profesor(id):
    return profesor_controller.ver_profesor(id)

@profesor_bp.route('/api/profesores/<int:id>/materias', methods=['GET'])
def materias_asignadas(id):
    return profesor_controller.materias_asignadas_profesor(id)

#########################################################################
@profesor_bp.route('/api/materias/<int:materia_id>/notas', methods=['GET'])
def obtener_notas_por_materia(materia_id):
    return profesor_controller.obtener_notas_por_materia(materia_id)

@profesor_bp.route('/api/materias/<int:materia_id>/notas', methods=['POST'])
def registrar_notas_por_materia(materia_id):
    return profesor_controller.registrar_notas_por_materia(materia_id)

#########################################################################
@profesor_bp.route('/api/materias/<int:materia_id>/asistencias', methods=['GET'])
def obtener_asistencias_por_materia(materia_id):
    return profesor_controller.obtener_asistencias_por_materia(materia_id)

# Ruta para registrar asistencia por materia
@profesor_bp.route('/api/materias/<int:materia_id>/asistencias', methods=['POST'])
def registrar_asistencias(materia_id):
    return profesor_controller.registrar_asistencias_por_materia(materia_id)
#########################################################################
@profesor_bp.route('/api/materias/<int:materia_id>/participaciones', methods=['GET'])
def obtener_participaciones_por_materia(materia_id):
    return profesor_controller.obtener_participaciones_por_materia(materia_id)

profesor_bp.route('/api/materias/<int:materia_id>/participaciones', methods=['POST'])(registrar_participaciones)

#########################################################################
@profesor_bp.route('/api/materias/<int:materia_id>/estudiantes', methods=['GET'])
def obtener_estudiantes_por_materia(materia_id):
    return profesor_controller.obtener_estudiantes_por_materia(materia_id)
