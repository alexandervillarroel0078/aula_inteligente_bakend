# /controllers/profesor_controller.py
from flask import Blueprint, jsonify, request
from models import db
from models.profesor import Profesor
from models.materia_profesor import MateriaProfesor
from models.gestion import Gestion
from models.alumno_grado import AlumnoGrado
from models.alumno import Alumno
from models.grado import Grado
from models.periodo import Periodo
from models.nivel import Nivel
from models.nota_trimestre import NotaTrimestre
from models.materia import Materia
from sqlalchemy.orm import joinedload
from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion
from sqlalchemy import func, case

profesor_bp = Blueprint('profesor_bp', __name__)

#funciona
def listar_profesores():
    profesores = Profesor.query.filter_by(estado='activo').order_by(Profesor.id.asc()).all()
    resultado = [
        {
            'id': p.id,
            'nombre': p.nombre,
            'apellido': p.apellido,
            'estado': p.estado
        } for p in profesores
    ]
    return jsonify(resultado), 200

#funciona
def ver_profesor(id):
    profesor = Profesor.query.get(id)
    if not profesor:
        return jsonify({'error': 'Profesor no encontrado'}), 404

    resultado = {
        'id': profesor.id,
        'nombre': profesor.nombre,
        'apellido': profesor.apellido,
        'estado': profesor.estado
    }
    return jsonify(resultado), 200

#funciona
def materias_asignadas_profesor(profesor_id):
    profesor = Profesor.query.get(profesor_id)
    if not profesor:
        return jsonify({'error': 'Profesor no encontrado'}), 404

    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({'error': 'No hay gestión activa'}), 404

    asignaciones = MateriaProfesor.query \
        .filter_by(profesor_id=profesor_id) \
        .join(MateriaProfesor.grado) \
        .filter(Grado.gestion_id == gestion_activa.id) \
        .join(MateriaProfesor.materia) \
        .join(Grado.nivel) \
        .all()

    materias = []
    for asignacion in asignaciones:
        materias.append({
            'materia_id': asignacion.materia.id,
            'materia': asignacion.materia.nombre,
            'grado_id': asignacion.grado.id, 
            'grado': asignacion.grado.nombre,
            'nivel_id': asignacion.grado.nivel.id,
            'nivel': asignacion.grado.nivel.nombre,
            'gestion': gestion_activa.anio
        })

    resultado = {
        'profesor': {
            'id': profesor.id,
            'nombre': profesor.nombre,
            'apellido': profesor.apellido,
            'estado': profesor.estado
        },
        'materias_asignadas': materias
    }

    return jsonify(resultado), 200

#funciona
def obtener_estudiantes_por_materia(profesor_id, materia_id):
    # Buscar gestión activa
    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({'error': 'No hay gestión activa'}), 404

    # Buscar asignaciones de esa materia en la gestión activa Y del profesor indicado
    asignaciones = MateriaProfesor.query \
        .join(Grado) \
        .filter(MateriaProfesor.materia_id == materia_id) \
        .filter(MateriaProfesor.profesor_id == profesor_id) \
        .filter(Grado.gestion_id == gestion_activa.id) \
        .all()

    if not asignaciones:
        return jsonify({'error': 'No se encontró la materia asignada al profesor en esta gestión'}), 404

    estudiantes = []
    total = 0

    profesor = asignaciones[0].profesor
    materia = asignaciones[0].materia

    for asignacion in asignaciones:
        alumnos_grado = AlumnoGrado.query \
            .filter_by(grado_id=asignacion.grado_id, estado='en curso') \
            .join(Alumno) \
            .all()

        for ag in alumnos_grado:
            estudiantes.append({
                'id': ag.alumno.id,
                'nombre': ag.alumno.nombre,
                'apellido': ag.alumno.apellido,
                'estado': ag.estado,
                'grado': asignacion.grado.nombre
            })
            total += 1

    return jsonify({
        'materia_id': materia.id,
        'materia': materia.nombre,
        'gestion': gestion_activa.anio,
        'profesor_id': profesor.id,
        'profesor': f'{profesor.nombre} {profesor.apellido}',
        'total_alumnos': total,
        'estudiantes': estudiantes
    }), 200

#funciona
def obtener_asistencias_por_grado():
    grado_id = request.args.get('grado_id', type=int)
    profesor_id = request.args.get('profesor_id', type=int)
    nivel_id = request.args.get('nivel', type=int)

    if not grado_id or not profesor_id or not nivel_id:
        return jsonify({'error': 'Faltan parámetros obligatorios'}), 400

    profesor = Profesor.query.get(profesor_id)
    grado = Grado.query.get(grado_id)

    if not profesor or not grado:
        return jsonify({'error': 'Datos no encontrados'}), 404

    gestion = grado.gestion
    nivel = grado.nivel

    periodos = Periodo.query.filter_by(gestion_id=gestion.id).all()
    periodos_data = []

    for periodo in periodos:
        query = HistorialAsistenciaParticipacion.query.filter_by(
            grado_id=grado_id,
            periodo_id=periodo.id,
            tipo='asistencia'
        )

        if nivel_id == 1:  # Primaria
            resultados = query.join(Alumno, Alumno.id == HistorialAsistenciaParticipacion.alumno_id).with_entities(
                HistorialAsistenciaParticipacion.alumno_id,
                Alumno.nombre,
                Alumno.apellido,
                func.count().label('total_registros'),
                func.sum(case((HistorialAsistenciaParticipacion.valor == 100, 1), else_=0)).label('asistencias_completas'),
                func.sum(case((HistorialAsistenciaParticipacion.valor == 80, 1), else_=0)).label('llegadas_tarde'),
                func.sum(case((HistorialAsistenciaParticipacion.valor == 50, 1), else_=0)).label('muy_tarde'),
                func.sum(case((HistorialAsistenciaParticipacion.valor == 1, 1), else_=0)).label('ausencias'),
                func.avg(HistorialAsistenciaParticipacion.valor).label('promedio_asistencia')
            ).group_by(
                HistorialAsistenciaParticipacion.alumno_id,
                Alumno.nombre,
                Alumno.apellido
            ).all()

            data = [
                {
                    'alumno_id': r.alumno_id,
                    'nombre': r.nombre,
                    'apellido': r.apellido,
                    'nombre_completo': f"{r.nombre} {r.apellido}",
                    'asistencias_completas': r.asistencias_completas,
                    'llegadas_tarde': r.llegadas_tarde,
                    'muy_tarde': r.muy_tarde,
                    'ausencias': r.ausencias,
                    'promedio_asistencia': round(r.promedio_asistencia, 2),
                    'total_clases': r.total_registros
                }
                for r in resultados
            ]

        else:  # Secundaria
            materias_docente = MateriaProfesor.query.filter_by(
                profesor_id=profesor_id,
                grado_id=grado_id
            ).with_entities(MateriaProfesor.materia_id).all()

            materias_ids = [m.materia_id for m in materias_docente]

            if not materias_ids:
                data = []
            else:
                resultados = query.join(Alumno, Alumno.id == HistorialAsistenciaParticipacion.alumno_id).filter(
                    HistorialAsistenciaParticipacion.materia_id.in_(materias_ids)
                ).with_entities(
                    HistorialAsistenciaParticipacion.alumno_id,
                    Alumno.nombre,
                    Alumno.apellido,
                    HistorialAsistenciaParticipacion.materia_id,
                    func.count().label('total_registros'),
                    func.sum(case((HistorialAsistenciaParticipacion.valor == 100, 1), else_=0)).label('asistencias_completas'),
                    func.sum(case((HistorialAsistenciaParticipacion.valor == 80, 1), else_=0)).label('llegadas_tarde'),
                    func.sum(case((HistorialAsistenciaParticipacion.valor == 50, 1), else_=0)).label('muy_tarde'),
                    func.sum(case((HistorialAsistenciaParticipacion.valor == 1, 1), else_=0)).label('ausencias'),
                    func.avg(HistorialAsistenciaParticipacion.valor).label('promedio_asistencia')
                ).group_by(
                    HistorialAsistenciaParticipacion.alumno_id,
                    HistorialAsistenciaParticipacion.materia_id,
                    Alumno.nombre,
                    Alumno.apellido
                ).all()

                data = [
                    {
                        'alumno_id': r.alumno_id,
                        'nombre': r.nombre,
                        'apellido': r.apellido,
                        'nombre_completo': f"{r.nombre} {r.apellido}",
                        'materia_id': r.materia_id,
                        'asistencias_completas': r.asistencias_completas,
                        'llegadas_tarde': r.llegadas_tarde,
                        'muy_tarde': r.muy_tarde,
                        'ausencias': r.ausencias,
                        'promedio_asistencia': round(r.promedio_asistencia, 2),
                        'total_clases': r.total_registros
                    }
                    for r in resultados
                ]

        periodos_data.append({
            'periodo_id': periodo.id,
            'nombre': periodo.nombre,
            'asistencias': data
        })

    return jsonify({
        'docente': {
            'id': profesor.id,
            'nombre': f'{profesor.nombre} {profesor.apellido}'
        },
        'grado': {
            'id': grado.id,
            'nombre': grado.nombre
        },
        'nivel': nivel.nombre,
        'gestion': gestion.anio,
        'periodos': periodos_data
    }), 200

#funciona
def obtener_participaciones_por_materia_por_grado():
    profesor_id = request.args.get('profesor_id', type=int)
    grado_id = request.args.get('grado_id', type=int)
    nivel_id = request.args.get('nivel_id', type=int)
    materia_id = request.args.get('materia_id', type=int)

    if not (profesor_id and grado_id and nivel_id and materia_id):
        return jsonify({'error': 'Faltan parámetros: profesor_id, grado_id, nivel_id o materia_id'}), 400

    gestion_activa = Gestion.query.filter_by(estado='activa').first()
    if not gestion_activa:
        return jsonify({'error': 'No hay gestión activa'}), 404

    periodos = Periodo.query.filter_by(gestion_id=gestion_activa.id).order_by(Periodo.id).all()
    if not periodos:
        return jsonify({'error': 'No hay periodos registrados en esta gestión'}), 404

    grado = Grado.query.get(grado_id)
    nivel = Nivel.query.get(nivel_id)
    materia = Materia.query.get(materia_id)

    if not grado or not nivel or not materia:
        return jsonify({'error': 'Grado, nivel o materia no encontrados'}), 404

    resultados = []
    TOTAL_ESPERADAS = 10

    alumnos = db.session.query(Alumno).join(AlumnoGrado).filter(
        AlumnoGrado.grado_id == grado_id
    ).all()

    for periodo in periodos:
        participaciones_alumnos = []

        for alumno in alumnos:
            cantidad = HistorialAsistenciaParticipacion.query.filter_by(
                tipo='participacion',
                grado_id=grado_id,
                periodo_id=periodo.id,
                alumno_id=alumno.id,
                materia_id=materia_id
            ).count()

            if cantidad == 0:
                continue

            no_participo = TOTAL_ESPERADAS - cantidad
            nota = round((cantidad / TOTAL_ESPERADAS) * 100, 2)

            participaciones_alumnos.append({
                'alumno_id': alumno.id,
                'nombre': alumno.nombre,
                'apellido': alumno.apellido,
                'participaciones_registradas': cantidad,
                'total_esperadas': TOTAL_ESPERADAS,
                'no_participo': no_participo,
                'nota_participacion': nota
            })

        # Siempre agregar el periodo, incluso si está vacío
        resultados.append({
            'periodo_id': periodo.id,
            'periodo': periodo.nombre,
            'participaciones': participaciones_alumnos
        })

    return jsonify({
        'profesor_id': profesor_id,
        'grado_id': grado_id,
        'materia_id': materia_id,
        'nombre_grado': grado.nombre,
        'nivel_id': nivel_id,
        'nombre_nivel': nivel.nombre,
        'materia': {
            'id': materia.id,
            'nombre': materia.nombre
        },
        'gestion': gestion_activa.anio,
        'participaciones_por_periodo': resultados
    })

#funciona
def obtener_notas_por_materia_por_grado():
    grado_id = request.args.get('grado_id', type=int)
    profesor_id = request.args.get('profesor_id', type=int)
    nivel_id = request.args.get('nivel_id', type=int)
    materia_id = request.args.get('materia_id', type=int)

    if not grado_id or not profesor_id or not nivel_id or not materia_id:
        return jsonify({'error': 'Faltan parámetros obligatorios'}), 400

    gestion = Gestion.query.filter_by(estado='activa').first()
    if not gestion:
        return jsonify({'error': 'No hay gestión activa'}), 404

    # Verifica que el profesor tiene asignada esa materia en ese grado y nivel
    materia_asignada = MateriaProfesor.query \
        .join(MateriaProfesor.materia) \
        .filter(
            MateriaProfesor.profesor_id == profesor_id,
            MateriaProfesor.grado_id == grado_id,
            MateriaProfesor.materia_id == materia_id,
            Materia.nivel_id == nivel_id
        ).first()

    if not materia_asignada:
        return jsonify({'error': 'Materia no asignada al profesor en este grado y nivel'}), 404

    materia = materia_asignada.materia
    profesor = materia_asignada.profesor
    grado = materia_asignada.grado

    periodos = Periodo.query.filter_by(gestion_id=gestion.id).all()

    data = {
        "docente": {
            "id": profesor.id,
            "nombre": f"{profesor.nombre} {profesor.apellido}"
        },
        "materia": {
            "id": materia.id,
            "nombre": materia.nombre
        },
        "grado": {
            "id": grado.id,
            "nombre": grado.nombre
        },
        "nivel": grado.nivel.nombre,
        "gestion": gestion.anio,
        "periodos": []
    }

    for periodo in periodos:
        notas = NotaTrimestre.query.options(joinedload(NotaTrimestre.alumno)) \
            .filter_by(
                grado_id=grado_id,
                materia_id=materia_id,
                periodo_id=periodo.id
            ).all()

        data["periodos"].append({
            "periodo_id": periodo.id,
            "nombre": periodo.nombre,
            "notas": [
                {
                    "alumno_id": n.alumno.id,
                    "nombre": n.alumno.nombre,
                    "apellido": n.alumno.apellido,
                    "nota_parcial": n.nota_parcial,
                    "asistencia_trimestre": n.asistencia_trimestre,
                    "participacion_trimestre": n.participacion_trimestre
                } for n in notas
            ]
        })

    return jsonify(data), 200

