from datetime import datetime
from flask import request, jsonify
from models import db
from models.profesor import Profesor
from models.materia_profesor import MateriaProfesor
from models.materia import Materia
from models.nota import Nota
from models.asistencia import Asistencia
from models.participacion import Participacion
from models.alumno import Alumno
from models.materia import Materia
from models.grado import Grado
from models.alumno_grado import AlumnoGrado
from collections import defaultdict
from sqlalchemy import func
 
from traits.bitacora_trait import registrar_bitacora
from models.parcial import Parcial
from models.periodo import Periodo
from sqlalchemy import func, cast, Numeric

def listar_profesores():
    profesores = Profesor.query.all()
    return jsonify([
        {
            "id": p.id,
            "codigo": p.codigo,
            "nombre_completo": p.nombre_completo,
            "ci": p.ci,
            "email": p.email,
            "telefono": p.telefono,
            "direccion": p.direccion,
            "estado": p.estado
        } for p in profesores
    ])

def ver_profesor(id):
    p = Profesor.query.get_or_404(id)
    return jsonify({
        "id": p.id,
        "codigo": p.codigo,
        "nombre_completo": p.nombre_completo,
        "ci": p.ci,
        "email": p.email,
        "telefono": p.telefono,
        "direccion": p.direccion,
        "estado": p.estado
    })

def materias_asignadas_profesor(profesor_id):
    relaciones = MateriaProfesor.query.filter_by(profesor_id=profesor_id).all()
    materias = []
    for r in relaciones:
        m = r.materia
        materias.append({
            "id": m.id,
            "codigo": m.codigo,
            "nombre": m.nombre,
            "descripcion": m.descripcion,
            "turno": m.turno,
            "aula": m.aula,
            "estado": m.estado,
            "fecha_asignacion": r.fecha_asignacion.isoformat() if r.fecha_asignacion else None
        })
    return jsonify(materias)

#las notas de un materia de cada alumno
def obtener_notas_por_materia(materia_id):
    materia = Materia.query.get_or_404(materia_id)

    # Obtener todas las notas de esa materia
    notas = Nota.query.filter_by(materia_id=materia.id).all()

    # Diccionario para agrupar por alumno
    agrupado_por_alumno = {}

    for nota in notas:
        alumno_id = nota.alumno.id
        if alumno_id not in agrupado_por_alumno:
            agrupado_por_alumno[alumno_id] = {
                "alumno_id": alumno_id,
                "alumno": nota.alumno.nombre_completo,
                "nota1": None,
                "nota2": None,
                "nota3": None,
                "nota4": None,
                "promedio": None  # lo calcularemos después si deseas
            }

        # Detectar qué bimestre es
        bimestre_map = {
            "1erP": "nota1",
            "2doP": "nota2",
            "3erP": "nota3",
            "4toP": "nota4"
        }

        campo = bimestre_map.get(nota.tipo_parcial)
        if campo:
            agrupado_por_alumno[alumno_id][campo] = nota.nota

    # Calcular promedio si hay al menos una nota
    for alumno_data in agrupado_por_alumno.values():
        notas_validas = [n for n in [alumno_data["nota1"], alumno_data["nota2"], alumno_data["nota3"], alumno_data["nota4"]] if n is not None]
        if notas_validas:
            alumno_data["promedio"] = round(sum(notas_validas) / len(notas_validas), 2)

    # Devolver como lista
    return jsonify(list(agrupado_por_alumno.values()))

#este memtodo esta mal arrenglar 
def registrar_notas_por_materia(materia_id):
    try:
        # Obtener los datos enviados en formato JSON
        data = request.get_json()
        notas = data['notas']  # Lista de notas de estudiantes

        # Crear un registro para cada nota de estudiante
        for nota_data in notas:
            alumno_id = nota_data['alumno_id']
            periodo_id = nota_data['periodo_id']
            parcial = nota_data['parcial']

            # Crear un nuevo registro de parcial para cada estudiante
            nuevo_parcial = Parcial(
                alumno_id=alumno_id,
                materia_id=materia_id,
                periodo_id=periodo_id,
                parcial=parcial
            )

            # Agregar a la base de datos
            db.session.add(nuevo_parcial)

        # Hacer commit para todas las notas
        db.session.commit()

        return jsonify({"message": "Notas registradas con éxito"}), 201  # Respuesta exitosa
    except Exception as e:
        db.session.rollback()  # En caso de error, revertir los cambios
        return jsonify({"error": str(e)}), 400  # Devolver el error


#las asistencia de un materia de cada alumno
def obtener_asistencias_por_materia(materia_id):
    alumnos = db.session.query(Alumno).\
        join(Asistencia, Alumno.id == Asistencia.alumno_id).\
        filter(Asistencia.materia_id == materia_id).\
        distinct().all()  # Asegúrate de que no se eliminen registros necesarios

    resultado = []

    for alumno in alumnos:
        asistencias = Asistencia.query.filter_by(materia_id=materia_id, alumno_id=alumno.id).all()

        # Inicializar las variables para contar asistencias y clases
        periodos = {1: 0, 2: 0, 3: 0, 4: 0}  # Contador de asistencias presentes por periodo
        clases_por_periodo = {1: 0, 2: 0, 3: 0, 4: 0}  # Total de clases por periodo
        total_asistencias = 0
        total_clases = 0

        # Recorrer las asistencias de cada alumno
        for asistencia in asistencias:
            pid = asistencia.periodo_id
            if pid in periodos:
                clases_por_periodo[pid] += 1  # Incrementar el total de clases para el periodo
                total_clases += 1  # Incrementar el total de clases generales
                if asistencia.presente:
                    periodos[pid] += 1  # Incrementar las asistencias presentes para el periodo
                    total_asistencias += 1  # Incrementar las asistencias generales

        # Calcular porcentajes de asistencia por bimestre (por periodo)
        porcentaje_periodo1 = round((periodos[1] / clases_por_periodo[1]) * 100, 2) if clases_por_periodo[1] > 0 else 0.0
        porcentaje_periodo2 = round((periodos[2] / clases_por_periodo[2]) * 100, 2) if clases_por_periodo[2] > 0 else 0.0
        porcentaje_periodo3 = round((periodos[3] / clases_por_periodo[3]) * 100, 2) if clases_por_periodo[3] > 0 else 0.0
        porcentaje_periodo4 = round((periodos[4] / clases_por_periodo[4]) * 100, 2) if clases_por_periodo[4] > 0 else 0.0

        # Calcular el porcentaje total de asistencia
        porcentaje_total = round((total_asistencias / total_clases) * 100, 2) if total_clases > 0 else 0.0

        # Agregar los datos del alumno al resultado
        resultado.append({
            "alumno": alumno.nombre_completo,
            "alumno_id": alumno.id,
            "periodo1": periodos[1],
            "periodo2": periodos[2],
            "periodo3": periodos[3],
            "periodo4": periodos[4],
            "total_clases": total_clases,
            "total_asistencias": total_asistencias,
            "porcentaje_asistencia": porcentaje_total,

            # Nuevos porcentajes por periodo
            "porcentaje_periodo1": porcentaje_periodo1,
            "porcentaje_periodo2": porcentaje_periodo2,
            "porcentaje_periodo3": porcentaje_periodo3,
            "porcentaje_periodo4": porcentaje_periodo4,
        })

    return jsonify(resultado)


def registrar_asistencias_por_materia(materia_id):
    data = request.get_json()

    fecha_str = data.get('fecha')
    periodo_id = data.get('periodo_id')
    asistencias = data.get('asistencias', [])

    if not fecha_str or not periodo_id or not asistencias:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Evitar duplicados: eliminamos registros previos del mismo día y materia
    Asistencia.query.filter_by(materia_id=materia_id, fecha=fecha, periodo_id=periodo_id).delete()
    db.session.commit()  # Realizamos el commit aquí después de eliminar los registros previos

    # Registrar las asistencias para todos los alumnos
    for asistencia in asistencias:
        nuevo = Asistencia(
            alumno_id=asistencia['alumno_id'],
            materia_id=materia_id,
            periodo_id=periodo_id,
            fecha=fecha,
            presente=asistencia['presente']
        )
        db.session.add(nuevo)

    db.session.commit()  # Commit después de agregar todos los registros

    # Actualizar el número de asistencias y clases por periodo
    for asistencia in asistencias:
        alumno_id = asistencia['alumno_id']
        alumno = Alumno.query.get(alumno_id)

        # Contamos el total de clases por periodo
        total_clases = Asistencia.query.filter_by(alumno_id=alumno_id, materia_id=materia_id, periodo_id=periodo_id).count()
        total_asistencias = Asistencia.query.filter_by(alumno_id=alumno_id, materia_id=materia_id, periodo_id=periodo_id, presente=True).count()

        porcentaje_asistencia = (total_asistencias / total_clases) * 100 if total_clases > 0 else 0

        # Actualizar los valores en el alumno
        alumno.porcentaje_asistencia = porcentaje_asistencia
        alumno.total_asistencias = total_asistencias
        alumno.total_clases = total_clases

        # Actualizar el porcentaje de asistencia por periodo
        if periodo_id == 1:
            alumno.porcentaje_periodo1 = porcentaje_asistencia
        elif periodo_id == 2:
            alumno.porcentaje_periodo2 = porcentaje_asistencia
        elif periodo_id == 3:
            alumno.porcentaje_periodo3 = porcentaje_asistencia
        elif periodo_id == 4:
            alumno.porcentaje_periodo4 = porcentaje_asistencia

    db.session.commit()  # Realizamos el commit después de actualizar todos los porcentajes

    return jsonify({"message": "Asistencias registradas correctamente"}), 201


#las participaciones de un materia de cada alumno
def obtener_participaciones_por_materia(materia_id):
    # Consultar todas las participaciones para esta materia, agrupadas por alumno y por periodo
    participaciones = db.session.query(
        Alumno.id.label('alumno_id'),
        Alumno.nombre_completo.label('alumno'),
        
        # Contar participaciones por periodo
        db.func.count(Participacion.id).filter(Participacion.periodo_id == 1).label('periodo1'),
        db.func.count(Participacion.id).filter(Participacion.periodo_id == 2).label('periodo2'),
        db.func.count(Participacion.id).filter(Participacion.periodo_id == 3).label('periodo3'),
        db.func.count(Participacion.id).filter(Participacion.periodo_id == 4).label('periodo4'),
        
        # Sumar puntajes por periodo
        db.func.sum(Participacion.puntaje).filter(Participacion.periodo_id == 1).label('nota_periodo1'),
        db.func.sum(Participacion.puntaje).filter(Participacion.periodo_id == 2).label('nota_periodo2'),
        db.func.sum(Participacion.puntaje).filter(Participacion.periodo_id == 3).label('nota_periodo3'),
        db.func.sum(Participacion.puntaje).filter(Participacion.periodo_id == 4).label('nota_periodo4'),
        
        # Total de participaciones por alumno
        db.func.count(Participacion.id).label('total_participaciones')
    ).join(Participacion, Participacion.alumno_id == Alumno.id) \
     .filter(Participacion.materia_id == materia_id) \
     .group_by(Alumno.id) \
     .all()

    resultado = []

    # Iterar sobre las participaciones y calcular las notas promedio
    for participacion in participaciones:
        
        # Asegurarse de que el total de las notas de cada periodo no sobrepase 100
        nota_periodo1 = min(participacion.nota_periodo1/ 4, 100) if participacion.nota_periodo1 else 0
        nota_periodo2 = min(participacion.nota_periodo2/ 4, 100) if participacion.nota_periodo2 else 0
        nota_periodo3 = min(participacion.nota_periodo3/ 4, 100) if participacion.nota_periodo3 else 0
        nota_periodo4 = min(participacion.nota_periodo4/ 4, 100) if participacion.nota_periodo4 else 0

        # Calcular el promedio de las notas de los 4 periodos
        promedio_total = (nota_periodo1 + nota_periodo2 + nota_periodo3 + nota_periodo4) / 4
        
        resultado.append({
            "alumno": participacion.alumno,
            "alumno_id": participacion.alumno_id,
            "periodo1": participacion.periodo1 or 0,
            "periodo2": participacion.periodo2 or 0,
            "periodo3": participacion.periodo3 or 0,
            "periodo4": participacion.periodo4 or 0,
            "nota_periodo1": nota_periodo1,
            "nota_periodo2": nota_periodo2,
            "nota_periodo3": nota_periodo3,
            "nota_periodo4": nota_periodo4,
            "nota_total_participaciones": round(promedio_total, 2),
            "total_participaciones": participacion.total_participaciones or 0
        })

    return jsonify(resultado)


def registrar_participaciones(materia_id):
    # Obtener los datos enviados desde el frontend
    data = request.get_json()

    fecha_str = data.get('fecha')
    periodo_id = data.get('periodo_id')
    participaciones = data.get('participaciones', [])

    # Validar los datos requeridos
    if not fecha_str or not periodo_id or not participaciones:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        # Convertir la fecha en formato adecuado (YYYY-MM-DD)
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    try:
        # Eliminar participaciones previas del mismo día y materia
        Participacion.query.filter_by(materia_id=materia_id, fecha=fecha, periodo_id=periodo_id).delete()
        db.session.commit()

        # Registrar las participaciones de los estudiantes
        for participacion in participaciones:
            # Verificar si los datos de la participación son correctos
            if not participacion.get('alumno_id') or not participacion.get('puntaje'):
                return jsonify({"error": "Faltan datos de la participación"}), 400

            # Crear la nueva participación
            nuevo = Participacion(
                alumno_id=participacion['alumno_id'],
                materia_id=materia_id,
                periodo_id=periodo_id,
                fecha=fecha,
                puntaje=participacion['puntaje']
            )

            # Añadir el objeto de participación a la sesión
            db.session.add(nuevo)

        # Confirmar cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Participaciones registradas correctamente"}), 201

    except Exception as e:
        # Deshacer los cambios en caso de error
        db.session.rollback()
        return jsonify({"error": f"Error al registrar participaciones: {str(e)}"}), 500



#todos los estudiantes de una materia
# En tu controlador, cambia la estructura de la respuesta de la siguiente manera:
def obtener_estudiantes_por_materia(materia_id):
    # Obtener la materia
    materia = Materia.query.get_or_404(materia_id)

    # Obtener el grado al que pertenece la materia
    grado = materia.grado

    # Obtener todos los alumnos asignados a ese grado
    alumnos_grado = AlumnoGrado.query.filter_by(grado_id=grado.id).all()

    estudiantes = []
    for ag in alumnos_grado:
        alumno = ag.alumno
        estudiantes.append({
            'alumno_id': alumno.id,
            'codigo': alumno.codigo,
            'nombre_completo': alumno.nombre_completo,
            'email': alumno.email,
            'telefono': alumno.telefono,
            'estado': alumno.estado,
            'grado_id': grado.id,
            'grado_nombre': grado.nombre,
            'nivel': grado.nivel,
            'paralelo': grado.paralelo,
            'seccion': grado.seccion,
            'turno': grado.turno,
            'gestion': ag.gestion
        })

    return jsonify({
        'total': len(estudiantes),
        'estudiantes': estudiantes
    })


