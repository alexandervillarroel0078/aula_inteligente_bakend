from flask import Blueprint, request
from controllers import profesor_controller
from controllers.profesor_controller import registrar_participaciones

profesor_bp = Blueprint('profesor_bp', __name__)

#http://localhost:5000/api/profesores
@profesor_bp.route('/api/profesores', methods=['GET'])
def listar_profesores():
    return profesor_controller.listar_profesores()

#http://localhost:5000/api/profesores/1
@profesor_bp.route('/api/profesores/<int:id>', methods=['GET'])
def obtener_profesor(id):
    return profesor_controller.ver_profesor(id)

#http://localhost:5000/api/profesores/1/materias
@profesor_bp.route('/api/profesores/<int:id>/materias', methods=['GET'])
def materias_asignadas(id):
    return profesor_controller.materias_asignadas_profesor(id)

#http://localhost:5000/api/notas/profesor?profesor_id=1&materia_id=1&grado_id=1
@profesor_bp.route('/api/notas/profesor', methods=['GET'])
def obtener_notas():
    return profesor_controller.obtener_notas_por_materia_profesor_grado()

#http://localhost:5000/api/participaciones/profesor?profesor_id=1&materia_id=1&grado_id=1&periodo_id=1
@profesor_bp.route('/api/participaciones/profesor', methods=['GET'])
def obtener_participacion():
    return profesor_controller.obtener_participacion_por_materia_profesor_grado()



#http://localhost:5000/api/asistencias/profesor/alumno?profesor_id=1&materia_id=1&grado_id=1&periodo_id=1
@profesor_bp.route('/api/asistencias/profesor/alumno', methods=['GET'])
def obtener_asistencias():
    return profesor_controller.obtener_asistencia_por_materia_profesor_grado()












#########################################################################
@profesor_bp.route('/api/materias/<int:materia_id>/notas', methods=['GET'])
def obtener_notas_por_materia(materia_id):
    return profesor_controller.obtener_notas_por_materia(materia_id)

# @profesor_bp.route('/api/materias/<int:materia_id>/notass', methods=['POST'])
# def registrar_notas_por_materia(materia_id):
#     return profesor_controller.registrar_notas_por_materia(materia_id)

#########################################################################
@profesor_bp.route('/api/materias/<int:materia_id>/asistencias', methods=['GET'])
def obtener_asistencias_por_materia(materia_id):
    return profesor_controller.obtener_asistencias_por_materia(materia_id)

# Ruta para registrar asistencia por materia
@profesor_bp.route('/api/materias/<int:materia_id>/asistencias', methods=['POST'])
def registrar_asistencias(materia_id):
    return profesor_controller.registrar_asistencias_por_materia(materia_id)


@profesor_bp.route('/api/materias/<int:materia_id>/notasFinalAsistencia', methods=['GET'])
def obtener_notas_final_asistencia_por_materia(materia_id):
    return profesor_controller.obtener_nota_final_asistencia_por_materia(materia_id)
   
#########################################################################
@profesor_bp.route('/api/materias/<int:materia_id>/participaciones', methods=['GET'])
def obtener_participaciones_por_materia(materia_id):
    return profesor_controller.obtener_participaciones_por_materia(materia_id)

profesor_bp.route('/api/materias/<int:materia_id>/participaciones', methods=['POST'])(registrar_participaciones)

#########################################################################
@profesor_bp.route('/api/materias/<int:materia_id>/estudiantes', methods=['GET'])
def obtener_estudiantes_por_materia(materia_id):
    return profesor_controller.obtener_estudiantes_por_materia(materia_id)
