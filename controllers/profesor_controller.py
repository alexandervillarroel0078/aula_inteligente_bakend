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
from collections import defaultdict
from sqlalchemy import func
from datetime import datetime
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
    # Obtener todas las notas de parciales por alumno y periodo
    parciales = db.session.query(
        Parcial.alumno_id,
        Alumno.nombre_completo.label("alumno"),
        Periodo.id.label("periodo_id"),
        func.round(func.avg(cast(Parcial.parcial, Numeric)), 2).label("nota")

    ).join(Alumno, Parcial.alumno_id == Alumno.id
    ).join(Periodo, Parcial.periodo_id == Periodo.id
    ).filter(Parcial.materia_id == materia_id
    ).group_by(Parcial.alumno_id, Alumno.nombre_completo, Periodo.id
    ).all()

    # Reorganizar los datos por alumno
    resultados = {}
    for p in parciales:
        alumno_id = p.alumno_id
        if alumno_id not in resultados:
            resultados[alumno_id] = {
                "alumno": p.alumno,
                "nota1": None,
                "nota2": None,
                "nota3": None,
                "nota4": None
            }

        if p.periodo_id == 1:
            resultados[alumno_id]["nota1"] = p.nota
        elif p.periodo_id == 2:
            resultados[alumno_id]["nota2"] = p.nota
        elif p.periodo_id == 3:
            resultados[alumno_id]["nota3"] = p.nota
        elif p.periodo_id == 4:
            resultados[alumno_id]["nota4"] = p.nota

    # Calcular el promedio general por alumno
    for alumno_id in resultados:
        notas = [resultados[alumno_id][f"nota{i}"] for i in range(1, 5)]
        notas_validas = [n for n in notas if n is not None]
        resultados[alumno_id]["promedio"] = round(sum(notas_validas) / len(notas_validas), 2) if notas_validas else None

    return jsonify(list(resultados.values()))

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
        distinct().all()

    resultado = []

    for alumno in alumnos:
        asistencias = Asistencia.query.filter_by(materia_id=materia_id, alumno_id=alumno.id).all()

        periodos = {1: 0, 2: 0, 3: 0, 4: 0}  # asistencias presentes
        clases_por_periodo = {1: 0, 2: 0, 3: 0, 4: 0}  # total de clases por periodo
        total_asistencias = 0
        total_clases = 0

        for asistencia in asistencias:
            pid = asistencia.periodo_id
            if pid in periodos:
                clases_por_periodo[pid] += 1
                total_clases += 1
                if asistencia.presente:
                    periodos[pid] += 1
                    total_asistencias += 1

        # Calcular porcentajes por bimestre
        porcentaje_periodo1 = round((periodos[1] / clases_por_periodo[1]) * 100, 2) if clases_por_periodo[1] > 0 else 0.0
        porcentaje_periodo2 = round((periodos[2] / clases_por_periodo[2]) * 100, 2) if clases_por_periodo[2] > 0 else 0.0
        porcentaje_periodo3 = round((periodos[3] / clases_por_periodo[3]) * 100, 2) if clases_por_periodo[3] > 0 else 0.0
        porcentaje_periodo4 = round((periodos[4] / clases_por_periodo[4]) * 100, 2) if clases_por_periodo[4] > 0 else 0.0

        porcentaje_total = round((total_asistencias / total_clases) * 100, 2) if total_clases > 0 else 0.0

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

            # NUEVO: porcentajes por periodo
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
    db.session.commit()

    for asistencia in asistencias:
        nuevo = Asistencia(
            alumno_id=asistencia['alumno_id'],
            materia_id=materia_id,
            periodo_id=periodo_id,
            fecha=fecha,
            presente=asistencia['presente']
        )
        db.session.add(nuevo)

    db.session.commit()

    return jsonify({"message": "Asistencias registradas correctamente"}), 201

#las participaciones de un materia de cada alumno
def obtener_participaciones_por_materia(materia_id):
    participaciones = Participacion.query.filter_by(materia_id=materia_id).all()
    return jsonify([
        {
            "id": p.id,
            "alumno": p.alumno.nombre_completo,
            "fecha": p.fecha.isoformat(),
            "puntaje": p.puntaje
        } for p in participaciones
    ])

#todos los estudiantes de una materia
def obtener_estudiantes_por_materia(materia_id):
    materia = Materia.query.get_or_404(materia_id)
    estudiantes = Alumno.query.filter_by(grado_id=materia.grado_id).all()

    datos = [
        {
            "id": alumno.id,
            "codigo": alumno.codigo,
            "nombre_completo": alumno.nombre_completo,
            "email": alumno.email,
            "telefono": alumno.telefono,
            "estado": alumno.estado
        } for alumno in estudiantes
    ]

    return jsonify({
        "total": len(estudiantes),
        "estudiantes": datos
    })




