
from flask import request, jsonify
from datetime import datetime
from traits.bitacora_trait import registrar_bitacora
from models import db
from models import Alumno, Nota, Asistencia, Participacion, Prediccion, Materia, MateriaProfesor
from models.materia import Materia
from models.nota import Nota
from models.periodo import Periodo
from models.alumno_grado import AlumnoGrado
from models.grado import Grado
from models.historial_asistencia_participacion import db, HistorialAsistenciaParticipacion
from flask import jsonify, abort

# CRUD básico
def listar_alumnos():
    # Obtener todos los alumnos
    alumnos = Alumno.query.all()
    
    resultado = [
        {
            'id': a.id,
            'codigo': a.codigo,
            'nombre_completo': a.nombre_completo,
            'fecha_nacimiento': a.fecha_nacimiento,
            'genero': a.genero,
            'email': a.email,
            'telefono': a.telefono,
            'direccion': a.direccion,
            'fecha_registro': a.fecha_registro,
            'estado': a.estado,
            'grados': [
                {
                    'id': ag.grado.id,
                    'nombre': ag.grado.nombre,
                    'nivel': ag.grado.nivel,
                    'seccion': ag.grado.seccion,
                    'paralelo': ag.grado.paralelo,
                    'turno': ag.grado.turno,
                    'gestion': ag.gestion
                }
                for ag in a.alumno_grados  # 'alumno_grados' es la relación con la tabla 'alumno_grado'
            ]
        }
        for a in alumnos
    ]
    
    return jsonify(resultado)
# ✅
def ver_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    
    # Obtener los grados asociados al alumno desde la tabla 'alumno_grado'
    grados = [
        {
            'id': ag.grado.id,
            'nombre': ag.grado.nombre,
            'nivel': ag.grado.nivel,
            'seccion': ag.grado.seccion,
            'paralelo': ag.grado.paralelo,
            'turno': ag.grado.turno,
            'gestion': ag.gestion
        }
        for ag in alumno.alumno_grados  # 'alumno_grados' es la relación con la tabla 'alumno_grado'
    ]
    
    return jsonify({
        'id': alumno.id,
        'codigo': alumno.codigo,
        'nombre_completo': alumno.nombre_completo,
        'fecha_nacimiento': alumno.fecha_nacimiento,
        'genero': alumno.genero,
        'email': alumno.email,
        'telefono': alumno.telefono,
        'direccion': alumno.direccion,
        'fecha_registro': alumno.fecha_registro,
        'estado': alumno.estado,
        'grados': grados  # Los grados asociados al alumno
    })
# ✅
def obtener_perfil_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    
    grados = [
        {
            'id': ag.grado.id,
            'nombre': ag.grado.nombre,
            'nivel': ag.grado.nivel,
            'seccion': ag.grado.seccion,
            'paralelo': ag.grado.paralelo,
            'turno': ag.grado.turno,
            'gestion': ag.gestion
        }
        for ag in alumno.alumno_grados
    ]
    
    return jsonify({
        "id": alumno.id,
        "codigo": alumno.codigo,
        "nombre_completo": alumno.nombre_completo,
        "fecha_nacimiento": alumno.fecha_nacimiento,
        "genero": alumno.genero,
        "email": alumno.email,
        "telefono": alumno.telefono,
        "direccion": alumno.direccion,
        "fecha_registro": alumno.fecha_registro,
        "estado": alumno.estado,
        "grados": grados
    })
# ✅
def obtener_notas_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    notas = Nota.query.filter_by(alumno_id=alumno.id).all()

    resultado = []
    for nota in notas:
        anio = nota.periodo.anio if nota.periodo else None
        gestion = nota.periodo.grado.gestion if nota.periodo and nota.periodo.grado else None
        grado = {
            'id': nota.periodo.grado.id if nota.periodo and nota.periodo.grado else None,
            'nombre': nota.periodo.grado.nombre if nota.periodo and nota.periodo.grado else None,
            'nivel': nota.periodo.grado.nivel if nota.periodo and nota.periodo.grado else None,
            'seccion': nota.periodo.grado.seccion if nota.periodo and nota.periodo.grado else None,
            'paralelo': nota.periodo.grado.paralelo if nota.periodo and nota.periodo.grado else None,
            'turno': nota.periodo.grado.turno if nota.periodo and nota.periodo.grado else None,
            'gestion': gestion
        }

        resultado.append({
            'id': nota.id,
            'materia_id': nota.materia_id,
            'materia_nombre': nota.materia.nombre if nota.materia else None,
            'periodo_id': nota.periodo_id,
            'periodo_nombre': nota.periodo.nombre if nota.periodo else None,
            'anio': anio,
            'gestion': gestion,
            'nota_periodo': nota.nota,
            'observaciones': nota.observaciones,
            'tipo_parcial': nota.tipo_parcial,
            'grado': grado,
            'grado_nombre': grado['nombre']
        })

    return jsonify(resultado)


########################################
# def obtener_asistencias_alumno():
#     return obtener_asistencias_historial()  # Llama al método que obtiene las asistencias del historial
# def obtener_asistencias_alumno():
#     # Obtener parámetros de la solicitud de los query params
#     alumno_id = request.args.get('alumno_id', type=int)
#     grado_id = request.args.get('grado_id', type=int)
    
#     if not alumno_id or not grado_id:
#         return jsonify({"message": "alumno_id y grado_id son requeridos"}), 400
    
#     # Filtrar historial por alumno_id, grado_id y tipo 'asistencia'
#     historial = HistorialAsistenciaParticipacion.query.filter_by(
#         alumno_id=alumno_id,
#         grado_id=grado_id,
#         tipo='asistencia'  # Solo registros de asistencia
#     ).all()

#     if not historial:
#         return jsonify({"message": "No se encontraron registros de asistencia para este alumno y grado"}), 404
    
#     # Calcular el total de asistencias y faltas por periodo
#     asistencia_por_periodo = {}
#     for h in historial:
#         # Si el periodo ya está en el diccionario, sumar el puntaje
#         if h.periodo_id not in asistencia_por_periodo:
#             asistencia_por_periodo[h.periodo_id] = {
#                 'total_asistencias': 0,
#                 'total_faltas': 0,
#                 'total_clases': 0,
#             }
        
#         # Sumamos la asistencia si el puntaje es 100
#         if h.puntaje == 100:
#             asistencia_por_periodo[h.periodo_id]['total_asistencias'] += 1
#         else:
#             asistencia_por_periodo[h.periodo_id]['total_faltas'] += 1
        
#         asistencia_por_periodo[h.periodo_id]['total_clases'] += 1
    
#     # Responder con la asistencia total por periodo
#     return jsonify({
#         "alumno_id": alumno_id,
#         "grado_id": grado_id,
#         "asistencia_por_periodo": asistencia_por_periodo
#     }), 200
# ✅
def obtener_asistencias_alumno():
    # Obtener solo el parámetro alumno_id de los query params
    alumno_id = request.args.get('alumno_id', type=int)
    
    if not alumno_id:
        return jsonify({"message": "alumno_id es requerido"}), 400
    
    # Obtener el nombre del alumno usando el alumno_id
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"message": "Alumno no encontrado"}), 404

    # Filtrar historial por alumno_id y tipo 'asistencia' (sin grado_id)
    historial = HistorialAsistenciaParticipacion.query.filter_by(
        alumno_id=alumno_id,
        tipo='asistencia'  # Solo registros de asistencia
    ).all()

    if not historial:
        return jsonify({"message": "No se encontraron registros de asistencia para este alumno"}), 404
    
    # Calcular el total de asistencias y faltas por periodo
    asistencia_por_periodo = {}
    for h in historial:
        # Obtener el nombre del grado y periodo usando los IDs
        grado = Grado.query.get(h.grado_id)  # Obtener grado por grado_id
        periodo = Periodo.query.get(h.periodo_id)  # Obtener periodo por periodo_id
        
        # Si el grado o el periodo no existen, lo omitimos
        if not grado or not periodo:
            continue
        
        # Si el periodo ya está en el diccionario, sumar el puntaje
        if h.periodo_id not in asistencia_por_periodo:
            asistencia_por_periodo[h.periodo_id] = {
                'nombre_periodo': periodo.nombre,  # Nombre del periodo
                'nombre_grado': grado.nombre,  # Nombre del grado
                'total_asistencias': 0,
                'total_faltas': 0,
                'total_clases': 0,
                'puntaje': 0  # Inicializamos el puntaje
            }
        
        # Sumamos la asistencia si el puntaje es 100
        if h.puntaje == 100:
            asistencia_por_periodo[h.periodo_id]['total_asistencias'] += 1
        else:
            asistencia_por_periodo[h.periodo_id]['total_faltas'] += 1
        
        asistencia_por_periodo[h.periodo_id]['total_clases'] += 1
    
    # Calculamos el puntaje para cada periodo
    for periodo_id, datos in asistencia_por_periodo.items():
        # Suponiendo que cada periodo tiene 40 clases
        total_clases = 40
        
        # Calculamos el puntaje como el porcentaje de clases a las que asistió
        puntaje = (datos['total_asistencias'] / total_clases) * 100
        asistencia_por_periodo[periodo_id]['puntaje'] = round(puntaje, 2)
    
    # Responder con la asistencia total por periodo y el puntaje
    return jsonify({
        "alumno_id": alumno_id,
        "alumno_nombre": alumno.nombre_completo,  # Incluyendo el nombre del alumno
        "asistencia_por_periodo": asistencia_por_periodo
    }), 200
# ✅
def obtener_participacion_alumno():
    # Obtener solo el parámetro alumno_id de los query params
    alumno_id = request.args.get('alumno_id', type=int)
    
    if not alumno_id:
        return jsonify({"message": "alumno_id es requerido"}), 400
    
    # Obtener el nombre del alumno usando el alumno_id
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"message": "Alumno no encontrado"}), 404

    # Filtrar historial por alumno_id y tipo 'participacion'
    historial = HistorialAsistenciaParticipacion.query.filter_by(
        alumno_id=alumno_id,
        tipo='participación'  # Solo registros de participación
    ).all()

    if not historial:
        return jsonify({"message": "No se encontraron registros de participación para este alumno"}), 404
    
    # Calcular el total de participaciones por periodo
    participacion_por_periodo = {}
    for h in historial:
        # Obtener el nombre del grado y periodo usando los IDs
        grado = Grado.query.get(h.grado_id)  # Obtener grado por grado_id
        periodo = Periodo.query.get(h.periodo_id)  # Obtener periodo por periodo_id
        
        # Si el grado o el periodo no existen, lo omitimos
        if not grado or not periodo:
            continue
        
        # Si el periodo ya está en el diccionario, sumar el puntaje
        if h.periodo_id not in participacion_por_periodo:
            participacion_por_periodo[h.periodo_id] = {
                'nombre_periodo': periodo.nombre,  # Nombre del periodo
                'nombre_grado': grado.nombre,  # Nombre del grado
                'total_participaciones': 0,  # Inicializamos el contador de participaciones válidas
                'total_faltas': 0,  # Inicializamos el contador de faltas
                'total_clases': 8,  # Suponemos que hay 8 participaciones posibles por periodo
                'puntaje': 0  # Inicializamos el puntaje total
            }
        
        # Si la nota es mayor a 0, lo consideramos una participación válida
        if h.puntaje > 0:
            participacion_por_periodo[h.periodo_id]['total_participaciones'] += 1
            participacion_por_periodo[h.periodo_id]['puntaje'] += h.puntaje  # Sumar el puntaje de la participación
        else:
            participacion_por_periodo[h.periodo_id]['total_faltas'] += 1
    
    # Calculamos el porcentaje de participación para cada periodo
    for periodo_id, datos in participacion_por_periodo.items():
        # Calculamos el puntaje de participación como el porcentaje de participaciones sobre las 8 posibles
        porcentaje_participacion = (datos['total_participaciones'] / 8) * 100
        participacion_por_periodo[periodo_id]['porcentaje_participacion'] = round(porcentaje_participacion, 2)
    
    # Responder con la participación total por periodo y el puntaje
    return jsonify({
        "alumno_id": alumno_id,
        "alumno_nombre": alumno.nombre_completo,  # Incluyendo el nombre del alumno
        "participacion_por_periodo": participacion_por_periodo
    }), 200
# ✅
def obtener_materias_alumno():
    # Obtener el parámetro alumno_id de los query params
    alumno_id = request.args.get('alumno_id', type=int)

    if not alumno_id:
        return jsonify({"message": "alumno_id es requerido"}), 400

    # Obtener el nombre del alumno usando el alumno_id
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"message": "Alumno no encontrado"}), 404

    # Filtrar las materias del alumno por grado y periodo
    materias_por_grado = {}

    alumno_grados = AlumnoGrado.query.filter_by(alumno_id=alumno_id).all()

    if not alumno_grados:
        return jsonify({"message": "No se encontraron grados para este alumno"}), 404

    for ag in alumno_grados:
        # Obtener el grado asociado
        grado = Grado.query.get(ag.grado_id)
        if not grado:
            continue

        # Obtener las materias del grado
        materias = Materia.query.filter_by(grado_id=ag.grado_id).all()

        # Crear una estructura de datos para guardar las materias por grado
        materias_por_grado[grado.nombre] = {
            'grado_nombre': grado.nombre,
            'materias': [] if materias else ['No hay materias asignadas para este grado.']  # Manejo de error
        }

        for materia in materias:
            materias_por_grado[grado.nombre]['materias'].append({
                'materia_nombre': materia.nombre,
                'materia_codigo': materia.codigo
            })

    return jsonify({
        "alumno_id": alumno_id,
        "alumno_nombre": alumno.nombre_completo,
        "materias_por_grado": materias_por_grado
    }), 200



#######################################
def obtener_participaciones_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    return jsonify([
        {
            "id": p.id,
            "materia_id": p.materia_id,
            "materia_nombre": p.materia.nombre if p.materia else None,
            "periodo_id": p.periodo_id,
            "periodo_nombre": p.periodo.nombre if p.periodo else None,
            "fecha": p.fecha,
            "puntaje": p.puntaje
        }
        for p in alumno.participaciones
    ])

def obtener_predicciones_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    return jsonify([
        {
            "id": p.id,
            "periodo_id": p.periodo_id,
            "periodo_nombre": p.periodo.nombre if p.periodo else None,
            "anio": p.periodo.fecha_inicio.year if p.periodo and p.periodo.fecha_inicio else None,
            "promedio_notas": p.promedio_notas,
            "porcentaje_asistencia": p.porcentaje_asistencia,
            "promedio_participaciones": p.promedio_participaciones,
            "resultado_predicho": p.resultado_predicho
        }
        for p in alumno.predicciones
    ])

def obtener_historial_alumno(alumno_id):
    # Obtener el alumno o lanzar un error 404 si no existe
    alumno = Alumno.query.get_or_404(alumno_id)

    # Obtener todas las notas del alumno
    notas = Nota.query.filter_by(alumno_id=alumno.id).all()

    # Lista para almacenar el historial del alumno
    historial = []

    # Iterar sobre las notas y obtener la información de cada materia, periodo y nota
    for nota in notas:
        # Obtener la materia relacionada con la nota
        materia = Materia.query.get(nota.materia_id)
        # Obtener el periodo relacionado con la nota
        periodo = Periodo.query.get(nota.periodo_id)

        # Obtener el grado asociado con la materia
        grado = Grado.query.get(materia.grado_id)

        # Agregar la información al historial
        historial.append({
            'materia_id': materia.id,
            'materia_nombre': materia.nombre,
            'periodo_id': periodo.id,
            'periodo_nombre': periodo.nombre,
            'nota': nota.nota,
            'observaciones': nota.observaciones,
            'grado_id': grado.id,
            'grado_nombre': grado.nombre,
            'semestre': periodo.semestre,  # Asumiendo que el semestre está en el periodo
            'anio': periodo.anio,          # Asumiendo que el año está en el periodo
        })

    # Devolver el historial del alumno como respuesta en formato JSON
    return jsonify(historial)


# def obtener_materias_alumno(alumno_id):
#     # Obtener el alumno o lanzar un error 404 si no existe
#     alumno = Alumno.query.get_or_404(alumno_id)

#     # Obtener los grados a los que está asignado el alumno
#     grados = AlumnoGrado.query.filter_by(alumno_id=alumno.id).all()

#     # Lista para almacenar las materias de cada grado
#     materias = []

#     # Iterar sobre los grados y obtener las materias relacionadas
#     for grado in grados:
#         # Obtener el grado
#         grado_obj = Grado.query.get(grado.grado_id)

#         # Obtener las materias asociadas con ese grado
#         for materia in grado_obj.materias:
#             materias.append({
#                 'materia_id': materia.id,
#                 'materia_nombre': materia.nombre,
#                 'grado_id': grado.grado_id,
#                 'grado_nombre': grado_obj.nombre,
#                 'turno': grado_obj.turno,  # Obtener el turno de la materia
#             })
    
#     # Devolver las materias del alumno como respuesta en formato JSON
#     return jsonify(materias)

# NO BORRAR
# ✅ Obtener notas por alumno y materia
def obtener_notas_por_materia(alumno_id, materia_id):
    # Consultar todas las notas del alumno en la materia especificada
    notas = Nota.query.filter_by(alumno_id=alumno_id, materia_id=materia_id).all()
    
    resultado = []
    
    for n in notas:
        # Se obtiene la información de cada nota relacionada con el parcial y el periodo
        resultado.append({
            'id': n.id,
            'tipo_parcial': n.tipo_parcial,
            'nota': n.nota,
            'observaciones': n.observaciones,
            'periodo_id': n.periodo_id,
            'periodo_nombre': n.periodo.nombre if n.periodo else None
        })
    
    # Si no se encuentran notas, se puede añadir una respuesta para cada parcial que falta
    if not notas:
        resultado.append({
            'id': None,
            'tipo_parcial': 'Primer Parcial',
            'nota': None,
            'observaciones': None,
            'periodo_id': 1,
            'periodo_nombre': '1er Bimestre'
        })
        resultado.append({
            'id': None,
            'tipo_parcial': 'Segundo Parcial',
            'nota': None,
            'observaciones': None,
            'periodo_id': 2,
            'periodo_nombre': '2do Bimestre'
        })
        resultado.append({
            'id': None,
            'tipo_parcial': 'Tercer Parcial',
            'nota': None,
            'observaciones': None,
            'periodo_id': 3,
            'periodo_nombre': '3er Bimestre'
        })
        resultado.append({
            'id': None,
            'tipo_parcial': 'Cuarto Parcial',
            'nota': None,
            'observaciones': None,
            'periodo_id': 4,
            'periodo_nombre': '4to Bimestre'
        })

    return jsonify(resultado)

# ✅ Obtener asistencias por alumno y materia
def obtener_asistencias_por_materia(alumno_id, materia_id):
    asistencias = Asistencia.query.filter_by(alumno_id=alumno_id, materia_id=materia_id).all()
    resultado = []
    for a in asistencias:
        resultado.append({
            'id': a.id,
            'fecha': a.fecha,
            'presente': a.presente,
            'periodo_id': a.periodo_id,
            'periodo_nombre': a.periodo.nombre if a.periodo else None
        })
    return jsonify(resultado)

# ✅ontener cantidad de asistencias total por alumno 
def obtener_asistencia_total(alumno_id, materia_id, periodo_id):
    # Verificar si el alumno, la materia y el periodo existen
    alumno = Alumno.query.get_or_404(alumno_id)
    materia = Materia.query.get_or_404(materia_id)
    
    # Definir los periodos (bimestres)
    periodos = {
        1: "1er Bimestre",
        2: "2do Bimestre",
        3: "3er Bimestre",
        4: "4to Bimestre"
    }
    
    # Inicializar el resultado para todos los periodos
    resultado = []
    
    for periodo_id in periodos.keys():
        # Obtener las asistencias del alumno para esa materia y periodo específico
        asistencias = Asistencia.query.filter_by(
            alumno_id=alumno_id, materia_id=materia_id, periodo_id=periodo_id
        ).all()
        
        # Calcular el total de asistencias (número de clases a las que asistió)
        total_asistencias = sum(1 for a in asistencias if a.presente)
        
        # Calcular el total de clases programadas (número de registros en 'asistencias')
        total_clases = len(asistencias)
        
        # Calcular el porcentaje de asistencia
        porcentaje_asistencia = (total_asistencias / total_clases * 100) if total_clases > 0 else 0
        
        # Agregar el bimestre al resultado
        resultado.append({
            "alumno_id": alumno.id,
            "materia_nombre": materia.nombre,
            "periodo_nombre": periodos[periodo_id],
            "total_asistencias": total_asistencias,
            "total_clases": total_clases,
            "porcentaje_asistencia": porcentaje_asistencia
        })
    
    return jsonify(resultado), 200

def obtener_detalle_asistencia(alumno_id, materia_id, periodo_id):
    try:
        # Consulta filtrando por alumno, materia y periodo
        asistencias = db.session.query(Asistencia).join(Materia).join(Periodo).filter(
            Asistencia.alumno_id == alumno_id,
            Asistencia.materia_id == materia_id,
            Asistencia.periodo_id == periodo_id
        ).all()

        # Si no hay registros, retorna un mensaje
        if not asistencias:
            return jsonify({"mensaje": "No se encontraron asistencias para este periodo."}), 404

        # Si hay resultados, devuelve las asistencias
        resultados = []
        for asistencia in asistencias:
            resultados.append({
                "id": asistencia.id,
                "materia": asistencia.materia.nombre,
                "fecha": asistencia.fecha.strftime("%a, %d %b %Y"),  # Formato de fecha
                "estado": "Presente" if asistencia.presente else "Ausente"
            })

        return jsonify(resultados), 200

    except Exception as e:
        return jsonify({"mensaje": "Ocurrió un error", "error": str(e)}), 500


