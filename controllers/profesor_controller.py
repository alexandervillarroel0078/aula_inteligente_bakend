from datetime import datetime
from flask import request, jsonify
from sqlalchemy import func, cast, Numeric
from models import db
from models.profesor import Profesor
from models.materia import Materia
from models.materia_profesor import MateriaProfesor
from models.nota import Nota
from models.asistencia import Asistencia
from models.participacion import Participacion
from models.alumno import Alumno
from models.grado import Grado
from models.alumno_grado import AlumnoGrado
from models.parcial import Parcial
from models.periodo import Periodo
from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion
from collections import defaultdict

from traits.bitacora_trait import registrar_bitacora

# ✅ principal profesores
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

# ✅ profesor-->materia
def materias_asignadas_profesor(profesor_id):
    # Obtener todas las asignaciones de materia para el profesor
    relaciones = MateriaProfesor.query.filter_by(profesor_id=profesor_id).all()
    
    # Crear una lista para almacenar las materias con los detalles
    materias = []
    for r in relaciones:
        # Obtener la materia asociada a la asignación
        m = r.materia
        
        # Acceder al grado de la materia
        grado_nombre = m.grado.nombre if m.grado else 'No asignado'
        
        materias.append({
            "id": m.id,
            "codigo": m.codigo,
            "nombre": m.nombre,
            "descripcion": m.descripcion,
            "turno": m.turno,
            "aula": m.aula,
            "grado_id": m.grado.id,
            "grado_nombre": grado_nombre,  # Aquí añadimos el nombre del grado de la materia
            "estado_asignacion": r.estado,  # Obtener el estado de la asignación de materia al profesor
            "fecha_asignacion": r.gestion
        })
    
    # Retornar las materias asignadas en formato JSON
    return jsonify(materias)
 
# ✅ profesor-->perfil
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

# ✅ profesor-->materia-->notas
def obtener_notas_por_materia_profesor_grado():
    # Obtener los parámetros de la solicitud
    profesor_id = request.args.get('profesor_id', type=int)
    materia_id = request.args.get('materia_id', type=int)
    grado_id = request.args.get('grado_id', type=int)
    periodo_id = request.args.get('periodo_id', type=int)  # Nuevo parámetro para periodo

    # Verificar si los parámetros están presentes
    if not profesor_id or not materia_id or not grado_id:
        return jsonify({"message": "profesor_id, materia_id y grado_id son requeridos"}), 400

    # Obtener el profesor por su ID
    profesor = Profesor.query.get(profesor_id)
    if not profesor:
        return jsonify({"message": "Profesor no encontrado"}), 404

    # Obtener la materia por su ID
    materia = Materia.query.get(materia_id)
    if not materia:
        return jsonify({"message": "Materia no encontrada"}), 404

    # Verificar si la materia está asignada al profesor en el grado específico
    materia_profesor = MateriaProfesor.query.filter_by(
        materia_id=materia_id,
        profesor_id=profesor_id
    ).first()
    
    if not materia_profesor:
        return jsonify({"message": "La materia no está asignada a este profesor"}), 404
    
    # Si no se pasa un periodo_id, obtenemos las notas de todos los periodos
    if periodo_id:
        # Filtrar las notas de los alumnos en la materia para el grado y el periodo específico
        notas = Nota.query.filter_by(materia_id=materia_id, grado_id=grado_id, periodo_id=periodo_id).all()
    else:
        # Si no se pasa periodo_id, obtenemos las notas de todos los periodos para ese grado y materia
        notas = Nota.query.filter_by(materia_id=materia_id, grado_id=grado_id).all()
    
    if not notas:
        return jsonify({"message": "No se encontraron notas para esta materia en el grado seleccionado"}), 404
    
    # Crear la lista de notas para devolverlas en la respuesta
    notas_alumnos = []
    for nota in notas:
        alumno = nota.alumno
        notas_alumnos.append({
            "id": alumno.id,
            "alumno_nombre": alumno.nombre_completo,
            "nota_parcial": nota.nota,
            "nota_participacion": nota.nota_participacion,
            "nota_asistencia": nota.nota_asistencia,
            "observaciones": nota.observaciones,
            "periodo": nota.periodo.nombre if nota.periodo else "N/A",
            "grado": nota.grado.nombre if nota.grado else "N/A"
        })

    return jsonify({
        "profesor_id": profesor.id,
        "profesor_nombre": profesor.nombre_completo,
        "materia_id": materia.id,
        "materia_nombre": materia.nombre,
        "grado_id": grado_id,
        "periodo_id": periodo_id if periodo_id else "Todos los periodos",
        "notas": notas_alumnos
    }), 200

# ✅ profesor-->materia-->participacion
def obtener_participacion_por_materia_profesor_grado():
    # Obtener los parámetros de la solicitud
    profesor_id = request.args.get('profesor_id', type=int)
    materia_id = request.args.get('materia_id', type=int)
    grado_id = request.args.get('grado_id', type=int)
    periodo_id = request.args.get('periodo_id', type=int)

    # Verificar si los parámetros están presentes
    if not profesor_id or not materia_id or not grado_id:
        return jsonify({"message": "profesor_id, materia_id y grado_id son requeridos"}), 400

    # Obtener el profesor por su ID
    profesor = Profesor.query.get(profesor_id)
    if not profesor:
        return jsonify({"message": "Profesor no encontrado"}), 404

    # Obtener la materia por su ID
    materia = Materia.query.get(materia_id)
    if not materia:
        return jsonify({"message": "Materia no encontrada"}), 404

    # Verificar si la materia está asignada al profesor en el grado específico
    materia_profesor = MateriaProfesor.query.filter_by(
        materia_id=materia_id,
        profesor_id=profesor_id
    ).first()

    if not materia_profesor:
        return jsonify({"message": "La materia no está asignada a este profesor"}), 404

    # Obtener todos los alumnos del grado especificado
    alumnos_grado = AlumnoGrado.query.filter_by(grado_id=grado_id).all()

    if not alumnos_grado:
        return jsonify({"message": "No se encontraron alumnos para este grado"}), 404

    # Crear una lista de participaciones para todos los alumnos
    participaciones_totales = []

    for alumno_grado in alumnos_grado:
        alumno = alumno_grado.alumno  # Obtener el alumno asociado
        
        # Filtrar las participaciones de cada alumno en la materia y grado especificados
        historial = HistorialAsistenciaParticipacion.query.filter_by(
            alumno_id=alumno.id,
            materia_id=materia_id,
            grado_id=grado_id,
            tipo='participación'  # Solo registros de participación
        ).all()

        if not historial:
            continue  # Si no tiene participaciones, pasar al siguiente alumno
        
        # Calcular la participación por periodo
        participacion_por_periodo = {}
        for h in historial:
            grado = Grado.query.get(h.grado_id)  # Obtener grado por grado_id
            periodo = Periodo.query.get(h.periodo_id)  # Obtener periodo por periodo_id
            
            if not grado or not periodo:
                continue

            # Usamos un valor fijo para el total de clases por periodo, ya que no existe el campo 'total_clases'
            total_clases = 8  # Asumimos que siempre hay 8 clases por periodo (puedes ajustar esto si es necesario)

            if h.periodo_id not in participacion_por_periodo:
                participacion_por_periodo[h.periodo_id] = {
                    'nombre_periodo': periodo.nombre,
                    'nombre_grado': grado.nombre,
                    'total_participaciones': 0,
                    'total_faltas': 0,
                    'total_clases': total_clases,  # Usando un valor fijo
                    'puntaje': 0
                }

            # Si la participación tiene puntaje mayor que 0, se cuenta como participación válida
            if h.puntaje > 0:
                participacion_por_periodo[h.periodo_id]['total_participaciones'] += 1
                participacion_por_periodo[h.periodo_id]['puntaje'] += h.puntaje
            else:
                participacion_por_periodo[h.periodo_id]['total_faltas'] += 1
        
        # Calcular el porcentaje de participación por cada periodo
        for periodo_id, datos in participacion_por_periodo.items():
            porcentaje_participacion = (datos['total_participaciones'] / datos['total_clases']) * 100
            participacion_por_periodo[periodo_id]['porcentaje_participacion'] = round(porcentaje_participacion, 2)
        
        # Agregar los datos de participación del alumno a la lista
        participaciones_totales.append({
            "alumno_id": alumno.id,
            "alumno_nombre": alumno.nombre_completo,
            "participacion_por_periodo": participacion_por_periodo
        })

    return jsonify({
        "profesor_id": profesor.id,
        "profesor_nombre": profesor.nombre_completo,
        "materia_id": materia.id,
        "materia_nombre": materia.nombre,
        "grado_id": grado_id,
        "periodo_id": periodo_id if periodo_id else "Todos los periodos",
        "participaciones": participaciones_totales
    }), 200









def obtener_notas_por_materia(materia_id):
    materia = Materia.query.get_or_404(materia_id)
    notas = Nota.query.filter_by(materia_id=materia.id).all()
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
                "promedio": None
            }

        bimestre_map = {
            "1erP": "nota1",
            "2doP": "nota2",
            "3erP": "nota3",
            "4toP": "nota4"
        }

        campo = bimestre_map.get(nota.tipo_parcial)
        if campo:
            agrupado_por_alumno[alumno_id][campo] = nota.nota

    for alumno_data in agrupado_por_alumno.values():
        notas_validas = [n for n in [alumno_data["nota1"], alumno_data["nota2"], alumno_data["nota3"], alumno_data["nota4"]] if n is not None]
        if notas_validas:
            alumno_data["promedio"] = round(sum(notas_validas) / len(notas_validas), 2)

    return jsonify(list(agrupado_por_alumno.values()))

def registrar_notas_por_materia(materia_id):
    try:
        data = request.get_json()
        notas = data['notas']

        for nota_data in notas:
            alumno_id = nota_data['alumno_id']
            periodo_id = nota_data['periodo_id']
            parcial = nota_data['parcial']

            nuevo_parcial = Parcial(
                alumno_id=alumno_id,
                materia_id=materia_id,
                periodo_id=periodo_id,
                parcial=parcial
            )

            db.session.add(nuevo_parcial)

        db.session.commit()

        return jsonify({"message": "Notas registradas con éxito"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

#ASISTENCIAS
def obtener_asistencias_por_materia(materia_id):
    alumnos = db.session.query(Alumno).join(Asistencia).filter(Asistencia.materia_id == materia_id).distinct().all()

    resultado = []

    for alumno in alumnos:
        asistencias = Asistencia.query.filter_by(materia_id=materia_id, alumno_id=alumno.id, presente=True).all()

        asistencias_por_periodo = {1: 0, 2: 0, 3: 0, 4: 0}
        total_clases = 0

        for asistencia in asistencias:
            pid = asistencia.periodo_id
            if pid in asistencias_por_periodo:
                asistencias_por_periodo[pid] += 1
                total_clases += 1
        
        resultado.append({
            "alumno": alumno.nombre_completo,
            "periodo1": asistencias_por_periodo[1],
            "periodo2": asistencias_por_periodo[2],
            "periodo3": asistencias_por_periodo[3],
            "periodo4": asistencias_por_periodo[4],
            "total_clases": total_clases,
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

    for asistencia in asistencias:
        alumno_id = asistencia['alumno_id']
        alumno = Alumno.query.get(alumno_id)

        total_clases = Asistencia.query.filter_by(alumno_id=alumno_id, materia_id=materia_id, periodo_id=periodo_id).count()
        total_asistencias = Asistencia.query.filter_by(alumno_id=alumno_id, materia_id=materia_id, periodo_id=periodo_id, presente=True).count()

        porcentaje_asistencia = (total_asistencias / total_clases) * 100 if total_clases > 0 else 0

        alumno.porcentaje_asistencia = porcentaje_asistencia
        alumno.total_asistencias = total_asistencias
        alumno.total_clases = total_clases

        if periodo_id == 1:
            alumno.porcentaje_periodo1 = porcentaje_asistencia
        elif periodo_id == 2:
            alumno.porcentaje_periodo2 = porcentaje_asistencia
        elif periodo_id == 3:
            alumno.porcentaje_periodo3 = porcentaje_asistencia
        elif periodo_id == 4:
            alumno.porcentaje_periodo4 = porcentaje_asistencia

    db.session.commit()

    return jsonify({"message": "Asistencias registradas correctamente"}), 201

def obtener_asistencias_por_bimestre(alumno_id, periodo_id):
    asistencias = db.session.query(Asistencia).filter_by(alumno_id=alumno_id, periodo_id=periodo_id).all()
    total_asistencias = len(asistencias)
    return total_asistencias

def obtener_nota_final_asistencia_por_materia(materia_id):
    resultado = []
    
    materia = Materia.query.get(materia_id)
    
    if not materia:
        return {'error': 'Materia no encontrada'}, 404
    
    alumnos = Alumno.query.join(Asistencia).filter(Asistencia.materia_id == materia_id).all()
    
    for alumno in alumnos:
        total_asistencias = db.session.query(Asistencia).filter_by(alumno_id=alumno.id, materia_id=materia_id, presente=True).count()
        
        nota_final_asistencia = (total_asistencias / 35) * 20
        
        resultado.append({
            'alumno_id': alumno.id,
            'nombre_alumno': alumno.nombre_completo,
            'materia': materia.nombre,
            'total_asistencias': total_asistencias,
            'nota_final_asistencia': round(nota_final_asistencia, 2)
        })
    
    return resultado

#PARTICIPACIONES
def obtener_participaciones_por_materia(materia_id):
    participaciones = db.session.query(
        Alumno.id.label('alumno_id'),
        Alumno.nombre_completo.label('alumno'),
        db.func.count(Participacion.id).filter(Participacion.periodo_id == 1).label('periodo1'),
        db.func.count(Participacion.id).filter(Participacion.periodo_id == 2).label('periodo2'),
        db.func.count(Participacion.id).filter(Participacion.periodo_id == 3).label('periodo3'),
        db.func.count(Participacion.id).filter(Participacion.periodo_id == 4).label('periodo4'),
        db.func.sum(Participacion.puntaje).filter(Participacion.periodo_id == 1).label('nota_periodo1'),
        db.func.sum(Participacion.puntaje).filter(Participacion.periodo_id == 2).label('nota_periodo2'),
        db.func.sum(Participacion.puntaje).filter(Participacion.periodo_id == 3).label('nota_periodo3'),
        db.func.sum(Participacion.puntaje).filter(Participacion.periodo_id == 4).label('nota_periodo4'),
        db.func.count(Participacion.id).label('total_participaciones')
    ).join(Participacion, Participacion.alumno_id == Alumno.id) \
     .filter(Participacion.materia_id == materia_id) \
     .group_by(Alumno.id) \
     .all()

    resultado = []

    for participacion in participaciones:
        nota_periodo1 = min(participacion.nota_periodo1 / 4, 100) if participacion.nota_periodo1 else 0
        nota_periodo2 = min(participacion.nota_periodo2 / 4, 100) if participacion.nota_periodo2 else 0
        nota_periodo3 = min(participacion.nota_periodo3 / 4, 100) if participacion.nota_periodo3 else 0
        nota_periodo4 = min(participacion.nota_periodo4 / 4, 100) if participacion.nota_periodo4 else 0

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
    data = request.get_json()

    fecha_str = data.get('fecha')
    periodo_id = data.get('periodo_id')
    participaciones = data.get('participaciones', [])

    if not fecha_str or not periodo_id or not participaciones:
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    try:
        Participacion.query.filter_by(materia_id=materia_id, fecha=fecha, periodo_id=periodo_id).delete()
        db.session.commit()

        for participacion in participaciones:
            if not participacion.get('alumno_id') or not participacion.get('puntaje'):
                return jsonify({"error": "Faltan datos de la participación"}), 400

            nuevo = Participacion(
                alumno_id=participacion['alumno_id'],
                materia_id=materia_id,
                periodo_id=periodo_id,
                fecha=fecha,
                puntaje=participacion['puntaje']
            )
            db.session.add(nuevo)

        db.session.commit()

        return jsonify({"message": "Participaciones registradas correctamente"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar participaciones: {str(e)}"}), 500

#ESTUDIANTES
def obtener_estudiantes_por_materia(materia_id):
    materia = Materia.query.get_or_404(materia_id)
    grado = materia.grado
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
