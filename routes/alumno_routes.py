from flask import Blueprint, request
from controllers import alumno_controller

# Usamos url_prefix para evitar repetir /api/alumnos
alumno_bp = Blueprint('alumno_bp', __name__, url_prefix='/api/alumnos')

# CRUD
@alumno_bp.route('/', methods=['GET'])
def listar_alumnos():
    return alumno_controller.listar_alumnos()

@alumno_bp.route('/<int:id>', methods=['GET'])
def ver_alumno(id):
    return alumno_controller.ver_alumno(id)

# Funcionalidades del alumno
#http://localhost:5000/api/alumnos//1/perfil
@alumno_bp.route('/<int:alumno_id>/perfil', methods=['GET'])
def obtener_perfil_alumno(alumno_id):
    return alumno_controller.obtener_perfil_alumno(alumno_id)

#http://localhost:5000/api/alumnos//1/notas
@alumno_bp.route('/<int:alumno_id>/notas', methods=['GET'])
def obtener_notas_alumno(alumno_id):
    return alumno_controller.obtener_notas_alumno(alumno_id)


#http://localhost:5000/api/alumnos/asistencias?alumno_id=1
@alumno_bp.route('/asistencias', methods=['GET'])
def obtener_asistencias_alumno():
    return alumno_controller.obtener_asistencias_alumno()

#http://localhost:5000/api/alumnos/participacion?alumno_id=1
@alumno_bp.route('/participacion', methods=['GET'])
def obtener_participacion_alumno():
    return alumno_controller.obtener_participacion_alumno()

#http://localhost:5000/api/alumnos/materias?alumno_id=1
@alumno_bp.route('/materias', methods=['GET'])
def obtener_materias_alumno():
    return alumno_controller.obtener_materias_alumno()




@alumno_bp.route('/<int:alumno_id>/participaciones', methods=['GET'])
def obtener_participaciones_alumno(alumno_id):
    return alumno_controller.obtener_participaciones_alumno(alumno_id)

@alumno_bp.route('/<int:alumno_id>/predicciones', methods=['GET'])
def obtener_predicciones_alumno(alumno_id):
    return alumno_controller.obtener_predicciones_alumno(alumno_id)

@alumno_bp.route('/<int:alumno_id>/historial', methods=['GET'])
def obtener_historial_alumno(alumno_id):
    return alumno_controller.obtener_historial_alumno(alumno_id)


#http://127.0.0.1:5000/api/alumnos/1/materias/3/notas
@alumno_bp.route('/<int:alumno_id>/materias/<int:materia_id>/notas', methods=['GET'])
def obtener_notas_por_materia(alumno_id, materia_id):
    return alumno_controller.obtener_notas_por_materia(alumno_id, materia_id)

#http://127.0.0.1:5000/api/alumnos/1/materias/3/asistencias
@alumno_bp.route('/<int:alumno_id>/materias/<int:materia_id>/asistencias', methods=['GET'])
def obtener_asistencias_por_materia(alumno_id, materia_id):
    return alumno_controller.obtener_asistencias_por_materia(alumno_id, materia_id)

#http://localhost:5000/api/alumnos/1/materias/2/periodos/1/asistencia
@alumno_bp.route('/<int:alumno_id>/materias/<int:materia_id>/periodos/<int:periodo_id>/asistencia', methods=['GET'])
def asistencia_materia_alumno(alumno_id, materia_id, periodo_id):
    return alumno_controller.obtener_asistencia_total(alumno_id, materia_id, periodo_id)

#http://127.0.0.1:5000/api/alumnos/1/materias/2/periodos/1/asistencia/detalle
@alumno_bp.route('/<int:alumno_id>/materias/<int:materia_id>/periodos/<int:periodo_id>/asistencia/detalle', methods=['GET'])
def obtener_detalle_asistencia(alumno_id, materia_id, periodo_id):
    return alumno_controller.obtener_detalle_asistencia(alumno_id, materia_id, periodo_id)