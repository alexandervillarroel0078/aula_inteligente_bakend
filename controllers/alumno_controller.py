from flask import request, jsonify
from models.alumno import Alumno
from models.alumno_grado import AlumnoGrado
from models.grado import Grado
from models.gestion import Gestion
from models.materia_grado import MateriaGrado
from models.materia import Materia
from models.nota_trimestre import NotaTrimestre

from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion

#funciona
def listar_alumnos():
    alumnos = Alumno.query.all()

    lista_alumnos = [
        {
            'id': alumno.id,
            'nombre': alumno.nombre,
            'apellido': alumno.apellido,
        }
        for alumno in alumnos
    ]

    return jsonify(lista_alumnos), 200
#funciona
def ver_alumno(id):
    alumno = Alumno.query.get(id)
    
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    return jsonify({
        'id': alumno.id,
        'nombre': alumno.nombre,
        'apellido': alumno.apellido
    }), 200
#funciona
def obtener_perfil_alumno(id):
    alumno = Alumno.query.get(id)

    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    perfil = {
        'id': alumno.id,
        'nombre': alumno.nombre,
        'apellido': alumno.apellido,
        # Aquí puedes agregar más datos si lo deseas
    }

    return jsonify(perfil), 200
#funciona
def obtener_materias_por_alumno():
    alumno_id = request.args.get('alumno_id', type=int)

    if not alumno_id:
        return jsonify({'error': 'Falta el parámetro alumno_id'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    resultado = []

    for inscripcion in alumno.historial_grados:
        grado = inscripcion.grado
        gestion = grado.gestion

        materias = Materia.query\
            .join(MateriaGrado)\
            .filter(MateriaGrado.grado_id == grado.id)\
            .all()

        materias_list = [
            {
                'id': m.id,
                'nombre': m.nombre,
                'descripcion': m.descripcion
            } for m in materias
        ]

        resultado.append({
            'gestion': gestion.anio,
            'grado': grado.nombre,
            'estado': inscripcion.estado,
            'materias': materias_list
        })

    return jsonify({
        'alumno_nombre': f"{alumno.nombre} {alumno.apellido}",
        'materias_por_gestion': resultado
    }), 200
#funciona
# def obtener_asistencias_por_alumno():
#     alumno_id = request.args.get('alumno_id', type=int)
#     if not alumno_id:
#         return jsonify({'error': 'Falta el parámetro alumno_id'}), 400

#     alumno = Alumno.query.get(alumno_id)
#     if not alumno:
#         return jsonify({'error': 'Alumno no encontrado'}), 404

#     resultado = {
#         "alumno_nombre": f"{alumno.nombre} {alumno.apellido}",
#         "asistencias": {}
#     }

#     # Obtener TODAS las gestiones
#     gestiones = Gestion.query.all()

#     for gestion in gestiones:
#         gestion_anio = str(gestion.anio)
#         resultado["asistencias"][gestion_anio] = {
#             "estado": gestion.estado,
#             "grados": {}
#         }

#         for grado in gestion.grados:
#             grado_nombre = grado.nombre
#             resultado["asistencias"][gestion_anio]["grados"][grado_nombre] = {}

#             # Acceder a todos los periodos de esa gestión
#             for periodo in gestion.periodos:
#                 periodo_nombre = periodo.nombre

#                 if periodo_nombre not in resultado["asistencias"][gestion_anio]["grados"][grado_nombre]:
#                     resultado["asistencias"][gestion_anio]["grados"][grado_nombre][periodo_nombre] = {}

#                 # Acceder a todas las materias del grado
#                 for materia_grado in grado.materias_asignadas:
#                     materia = materia_grado.materia
#                     materia_nombre = materia.nombre

#                     # Inicializar lista vacía para la materia
#                     resultado["asistencias"][gestion_anio]["grados"][grado_nombre][periodo_nombre][materia_nombre] = []

#                     # Buscar asistencia si existe
#                     notas = NotaTrimestre.query.filter_by(
#                         alumno_id=alumno.id,
#                         grado_id=grado.id,
#                         materia_id=materia.id,
#                         periodo_id=periodo.id
#                     ).all()

#                     for nota in notas:
#                         if nota.asistencia_trimestre is not None:
#                             resultado["asistencias"][gestion_anio]["grados"][grado_nombre][periodo_nombre][materia_nombre].append({
#                                 "observaciones": "Extraído de nota trimestral",
#                                 "valor": nota.asistencia_trimestre
#                             })

#     return jsonify(resultado), 200

def obtener_asistencias_por_alumno():
    alumno_id = request.args.get('alumno_id', type=int)
    if not alumno_id:
        return jsonify({'error': 'Falta el parámetro alumno_id'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    resultado = {
        "alumno_nombre": f"{alumno.nombre} {alumno.apellido}",
        "asistencias": {}
    }

    notas = NotaTrimestre.query.filter_by(alumno_id=alumno.id).all()

    for nota in notas:
        if nota.asistencia_trimestre is None:
            continue  # ignorar si no hay asistencia registrada

        gestion = nota.grado.gestion
        gestion_anio = str(gestion.anio)
        estado = gestion.estado
        grado_nombre = nota.grado.nombre
        periodo_nombre = nota.periodo.nombre
        materia_nombre = nota.materia.nombre

        if gestion_anio not in resultado["asistencias"]:
            resultado["asistencias"][gestion_anio] = {
                "estado": estado,
                "grados": {}
            }

        grados = resultado["asistencias"][gestion_anio]["grados"]

        if grado_nombre not in grados:
            grados[grado_nombre] = {}

        if periodo_nombre not in grados[grado_nombre]:
            grados[grado_nombre][periodo_nombre] = {}

        if materia_nombre not in grados[grado_nombre][periodo_nombre]:
            grados[grado_nombre][periodo_nombre][materia_nombre] = []

        grados[grado_nombre][periodo_nombre][materia_nombre].append({
            "observaciones": "Extraído de nota trimestral",
            "valor": nota.asistencia_trimestre
        })

    return jsonify(resultado), 200




#funciona
def obtener_participacion_por_alumno():
    alumno_id = request.args.get('alumno_id', type=int)
    if not alumno_id:
        return jsonify({'error': 'Falta el parámetro alumno_id'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    resultado = {
        "alumno_nombre": f"{alumno.nombre} {alumno.apellido}",
        "participaciones": {}
    }

    notas = NotaTrimestre.query.filter_by(alumno_id=alumno.id).all()

    for nota in notas:
        if nota.participacion_trimestre is None:
            continue  # ignorar si no hay participación registrada

        gestion = nota.grado.gestion
        gestion_anio = str(gestion.anio)
        estado = gestion.estado
        grado_nombre = nota.grado.nombre
        periodo_nombre = nota.periodo.nombre
        materia_nombre = nota.materia.nombre

        if gestion_anio not in resultado["participaciones"]:
            resultado["participaciones"][gestion_anio] = {
                "estado": estado,
                "grados": {}
            }

        grados = resultado["participaciones"][gestion_anio]["grados"]

        if grado_nombre not in grados:
            grados[grado_nombre] = {}

        if periodo_nombre not in grados[grado_nombre]:
            grados[grado_nombre][periodo_nombre] = {}

        if materia_nombre not in grados[grado_nombre][periodo_nombre]:
            grados[grado_nombre][periodo_nombre][materia_nombre] = []

        grados[grado_nombre][periodo_nombre][materia_nombre].append({
            "observaciones": "Extraído de nota trimestral",
            "valor": nota.participacion_trimestre
        })

    return jsonify(resultado), 200



#funiona
def obtener_notas_alumno():
    alumno_id = request.args.get('alumno_id')
    if not alumno_id:
        return jsonify({'error': 'Parámetro alumno_id es requerido'}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    notas = NotaTrimestre.query.filter_by(alumno_id=alumno_id).all()

    resultado = {
        'alumno_nombre': f"{alumno.nombre} {alumno.apellido}",
        'notas': {}
    }

    for nota in notas:
        gestion = nota.grado.gestion
        gestion_anio = str(gestion.anio)
        estado = gestion.estado
        grado_nombre = nota.grado.nombre
        periodo_nombre = nota.periodo.nombre
        materia_nombre = nota.materia.nombre
        valor = nota.nota_parcial

        # Inicializar gestión si no existe
        if gestion_anio not in resultado['notas']:
            resultado['notas'][gestion_anio] = {
                'estado': estado,
                'grados': {}
            }

        grados = resultado['notas'][gestion_anio]['grados']

        # Inicializar grado si no existe
        if grado_nombre not in grados:
            grados[grado_nombre] = {}

        # Inicializar periodo si no existe
        if periodo_nombre not in grados[grado_nombre]:
            grados[grado_nombre][periodo_nombre] = {}

        # Inicializar materia como lista si no existe
        if materia_nombre not in grados[grado_nombre][periodo_nombre]:
            grados[grado_nombre][periodo_nombre][materia_nombre] = []

        # Agregar nota
        grados[grado_nombre][periodo_nombre][materia_nombre].append({
            'observaciones': 'Nota parcial',
            'valor': valor
        })

    return jsonify(resultado), 200








