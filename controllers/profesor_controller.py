# from datetime import datetime
# from flask import request, jsonify
# from sqlalchemy import func, cast, Numeric
# from models import db
# from models.profesor import Profesor
# from models.materia import Materia

# from models.nota_bimestre import Nota

# from models.alumno import Alumno
# from models.grado import Grado
# from models.alumno_grado import AlumnoGrado

# from models.periodo import Periodo
# from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion

# from traits.bitacora_trait import registrar_bitacora

# # ✅ principal profesores
# def listar_profesores():
#     profesores = Profesor.query.all()
#     return jsonify([
#         {
#             "id": p.id,
#             "codigo": p.codigo,
#             "nombre_completo": p.nombre_completo,
#             "ci": p.ci,
#             "email": p.email,
#             "telefono": p.telefono,
#             "direccion": p.direccion,
#             "estado": p.estado
#         } for p in profesores
#     ])

# # ✅ profesor-->materia
# def materias_asignadas_profesor(profesor_id):
#     # Obtener todas las asignaciones de materia para el profesor
#     relaciones = MateriaProfesor.query.filter_by(profesor_id=profesor_id).all()
    
#     # Crear una lista para almacenar las materias con los detalles
#     materias = []
#     for r in relaciones:
#         # Obtener la materia asociada a la asignación
#         m = r.materia
        
#         # Acceder al grado de la materia
#         grado_nombre = m.grado.nombre if m.grado else 'No asignado'
        
#         materias.append({
#             "id": m.id,
#             "codigo": m.codigo,
#             "nombre": m.nombre,
#             "descripcion": m.descripcion,
#             "turno": m.turno,
#             "aula": m.aula,
#             "grado_id": m.grado.id,
#             "grado_nombre": grado_nombre,  # Aquí añadimos el nombre del grado de la materia
#             "estado_asignacion": r.estado,  # Obtener el estado de la asignación de materia al profesor
#             "fecha_asignacion": r.gestion
#         })
    
#     # Retornar las materias asignadas en formato JSON
#     return jsonify(materias)
 
# # ✅ profesor-->perfil
# def ver_profesor(id):
#     p = Profesor.query.get_or_404(id)
#     return jsonify({
#         "id": p.id,
#         "codigo": p.codigo,
#         "nombre_completo": p.nombre_completo,
#         "ci": p.ci,
#         "email": p.email,
#         "telefono": p.telefono,
#         "direccion": p.direccion,
#         "estado": p.estado
#     })

# # ✅ profesor-->materia-->notas
# def obtener_notas_por_materia_profesor_grado():
#     # Obtener los parámetros de la solicitud
#     profesor_id = request.args.get('profesor_id', type=int)
#     materia_id = request.args.get('materia_id', type=int)
#     grado_id = request.args.get('grado_id', type=int)
#     periodo_id = request.args.get('periodo_id', type=int)  # Nuevo parámetro para periodo

#     # Verificar si los parámetros están presentes
#     if not profesor_id or not materia_id or not grado_id:
#         return jsonify({"message": "profesor_id, materia_id y grado_id son requeridos"}), 400

#     # Obtener el profesor por su ID
#     profesor = Profesor.query.get(profesor_id)
#     if not profesor:
#         return jsonify({"message": "Profesor no encontrado"}), 404

#     # Obtener la materia por su ID
#     materia = Materia.query.get(materia_id)
#     if not materia:
#         return jsonify({"message": "Materia no encontrada"}), 404

#     # Verificar si la materia está asignada al profesor en el grado específico
#     materia_profesor = MateriaProfesor.query.filter_by(
#         materia_id=materia_id,
#         profesor_id=profesor_id
#     ).first()
    
#     if not materia_profesor:
#         return jsonify({"message": "La materia no está asignada a este profesor"}), 404
    
#     # Si no se pasa un periodo_id, obtenemos las notas de todos los periodos
#     if periodo_id:
#         # Filtrar las notas de los alumnos en la materia para el grado y el periodo específico
#         notas = Nota.query.filter_by(materia_id=materia_id, grado_id=grado_id, periodo_id=periodo_id).all()
#     else:
#         # Si no se pasa periodo_id, obtenemos las notas de todos los periodos para ese grado y materia
#         notas = Nota.query.filter_by(materia_id=materia_id, grado_id=grado_id).all()
    
#     if not notas:
#         return jsonify({"message": "No se encontraron notas para esta materia en el grado seleccionado"}), 404
    
#     # Crear la lista de notas para devolverlas en la respuesta
#     notas_alumnos = []
#     for nota in notas:
#         alumno = nota.alumno
#         notas_alumnos.append({
#             "id": alumno.id,
#             "alumno_nombre": alumno.nombre_completo,
#             "nota_parcial": nota.nota,
#             "nota_participacion": nota.nota_participacion,
#             "nota_asistencia": nota.nota_asistencia,
#             "observaciones": nota.observaciones,
#             "periodo": nota.periodo.nombre if nota.periodo else "N/A",
#             "grado": nota.grado.nombre if nota.grado else "N/A"
#         })

#     return jsonify({
#         "profesor_id": profesor.id,
#         "profesor_nombre": profesor.nombre_completo,
#         "materia_id": materia.id,
#         "materia_nombre": materia.nombre,
#         "grado_id": grado_id,
#         "periodo_id": periodo_id if periodo_id else "Todos los periodos",
#         "notas": notas_alumnos
#     }), 200

# # ✅ profesor-->materia-->participacion
# def obtener_participacion_por_materia_profesor_grado():
#     # Obtener los parámetros de la solicitud
#     profesor_id = request.args.get('profesor_id', type=int)
#     materia_id = request.args.get('materia_id', type=int)
#     grado_id = request.args.get('grado_id', type=int)
#     periodo_id = request.args.get('periodo_id', type=int)

#     # Verificar si los parámetros están presentes
#     if not profesor_id or not materia_id or not grado_id:
#         return jsonify({"message": "profesor_id, materia_id y grado_id son requeridos"}), 400

#     # Obtener el profesor por su ID
#     profesor = Profesor.query.get(profesor_id)
#     if not profesor:
#         return jsonify({"message": "Profesor no encontrado"}), 404

#     # Obtener la materia por su ID
#     materia = Materia.query.get(materia_id)
#     if not materia:
#         return jsonify({"message": "Materia no encontrada"}), 404

#     # Verificar si la materia está asignada al profesor en el grado específico
#     materia_profesor = MateriaProfesor.query.filter_by(
#         materia_id=materia_id,
#         profesor_id=profesor_id
#     ).first()

#     if not materia_profesor:
#         return jsonify({"message": "La materia no está asignada a este profesor"}), 404

#     # Obtener todos los alumnos del grado especificado
#     alumnos_grado = AlumnoGrado.query.filter_by(grado_id=grado_id).all()

#     if not alumnos_grado:
#         return jsonify({"message": "No se encontraron alumnos para este grado"}), 404

#     # Crear una lista de participaciones para todos los alumnos
#     participaciones_totales = []

#     for alumno_grado in alumnos_grado:
#         alumno = alumno_grado.alumno  # Obtener el alumno asociado
        
#         # Filtrar las participaciones de cada alumno en la materia y grado especificados
#         historial = HistorialAsistenciaParticipacion.query.filter_by(
#             alumno_id=alumno.id,
#             materia_id=materia_id,
#             grado_id=grado_id,
#             tipo='participación'  # Solo registros de participación
#         ).all()

#         if not historial:
#             continue  # Si no tiene participaciones, pasar al siguiente alumno
        
#         # Calcular la participación por periodo
#         participacion_por_periodo = {}
#         for h in historial:
#             grado = Grado.query.get(h.grado_id)  # Obtener grado por grado_id
#             periodo = Periodo.query.get(h.periodo_id)  # Obtener periodo por periodo_id
            
#             if not grado or not periodo:
#                 continue

#             # Usamos un valor fijo para el total de clases por periodo, ya que no existe el campo 'total_clases'
#             total_clases = 8  # Asumimos que siempre hay 8 clases por periodo (puedes ajustar esto si es necesario)

#             if h.periodo_id not in participacion_por_periodo:
#                 participacion_por_periodo[h.periodo_id] = {
#                     'nombre_periodo': periodo.nombre,
#                     'nombre_grado': grado.nombre,
#                     'total_participaciones': 0,
#                     'total_faltas': 0,
#                     'total_clases': total_clases,  # Usando un valor fijo
#                     'puntaje': 0
#                 }

#             # Si la participación tiene puntaje mayor que 0, se cuenta como participación válida
#             if h.puntaje > 0:
#                 participacion_por_periodo[h.periodo_id]['total_participaciones'] += 1
#                 participacion_por_periodo[h.periodo_id]['puntaje'] += h.puntaje
#             else:
#                 participacion_por_periodo[h.periodo_id]['total_faltas'] += 1
        
#         # Calcular el porcentaje de participación por cada periodo
#         for periodo_id, datos in participacion_por_periodo.items():
#             porcentaje_participacion = (datos['total_participaciones'] / datos['total_clases']) * 100
#             participacion_por_periodo[periodo_id]['porcentaje_participacion'] = round(porcentaje_participacion, 2)
        
#         # Agregar los datos de participación del alumno a la lista
#         participaciones_totales.append({
#             "alumno_id": alumno.id,
#             "alumno_nombre": alumno.nombre_completo,
#             "participacion_por_periodo": participacion_por_periodo
#         })

#     return jsonify({
#         "profesor_id": profesor.id,
#         "profesor_nombre": profesor.nombre_completo,
#         "materia_id": materia.id,
#         "materia_nombre": materia.nombre,
#         "grado_id": grado_id,
#         "periodo_id": periodo_id if periodo_id else "Todos los periodos",
#         "participaciones": participaciones_totales
#     }), 200

# # ✅ profesor-->materia-->asistencia
# def obtener_asistencia_por_materia_profesor_grado():
#     # Obtener los parámetros de la consulta (query params)
#     profesor_id = request.args.get('profesor_id', type=int)
#     materia_id = request.args.get('materia_id', type=int)
#     grado_id = request.args.get('grado_id', type=int)
#     periodo_id = request.args.get('periodo_id', type=int)

#     # Verificar si los parámetros están presentes
#     if not profesor_id or not materia_id or not grado_id:
#         return jsonify({"message": "profesor_id, materia_id y grado_id son requeridos"}), 400

#     # Obtener el profesor por su ID
#     profesor = Profesor.query.get(profesor_id)
#     if not profesor:
#         return jsonify({"message": "Profesor no encontrado"}), 404

#     # Obtener la materia por su ID
#     materia = Materia.query.get(materia_id)
#     if not materia:
#         return jsonify({"message": "Materia no encontrada"}), 404

#     # Verificar si la materia está asignada al profesor en el grado específico
#     materia_profesor = MateriaProfesor.query.filter_by(
#         materia_id=materia_id,
#         profesor_id=profesor_id
#     ).first()

#     if not materia_profesor:
#         return jsonify({"message": "La materia no está asignada a este profesor"}), 404

#     # Obtener todos los alumnos del grado especificado
#     alumnos_grado = AlumnoGrado.query.filter_by(grado_id=grado_id).all()

#     if not alumnos_grado:
#         return jsonify({"message": "No se encontraron alumnos para este grado"}), 404

#     # Crear una lista de asistencias para todos los alumnos
#     asistencias_totales = []

#     for alumno_grado in alumnos_grado:
#         alumno = alumno_grado.alumno  # Obtener el alumno asociado
        
#         # Filtrar las asistencias de cada alumno en la materia y grado especificados
#         historial = HistorialAsistenciaParticipacion.query.filter_by(
#             alumno_id=alumno.id,
#             materia_id=materia_id,
#             grado_id=grado_id,
#             tipo='asistencia'  # Solo registros de asistencia
#         ).all()

#         if not historial:
#             continue  # Si no tiene asistencias, pasar al siguiente alumno
        
#         # Calcular la asistencia por periodo
#         for h in historial:
#             grado = Grado.query.get(h.grado_id)  # Obtener grado por grado_id
#             periodo = Periodo.query.get(h.periodo_id)  # Obtener periodo por periodo_id
            
#             if not grado or not periodo:
#                 continue

#             # Usamos un valor fijo para el total de clases por periodo, ya que no existe el campo 'total_clases'
#             total_clases = 40  # Asumimos que siempre hay 40 clases por periodo (puedes ajustar esto si es necesario)

#             # Creamos la estructura por periodo, directamente
#             asistencia_por_periodo = {
#                 'alumno_id': alumno.id,
#                 'alumno_nombre': alumno.nombre_completo,
#                 'nombre_grado': grado.nombre,
#                 'grado_id': grado.id,  # Incluyendo el ID del grado
#                 'nombre_periodo': periodo.nombre,
#                 'periodo_id': periodo.id,  # Incluyendo el ID del periodo
#                 'total_asistencias': 0,
#                 'total_faltas': 0,
#                 'total_clases': total_clases,  # Usando un valor fijo de 40 clases
#                 'puntaje': 0
#             }

#             # Si la asistencia tiene puntaje igual a 100, se cuenta como asistencia válida
#             if h.puntaje == 100:
#                 asistencia_por_periodo['total_asistencias'] += 1
#             else:
#                 asistencia_por_periodo['total_faltas'] += 1

#             # Calcular el porcentaje de asistencia por cada periodo
#             porcentaje_asistencia = (asistencia_por_periodo['total_asistencias'] / total_clases) * 100
#             asistencia_por_periodo['porcentaje_asistencia'] = round(porcentaje_asistencia, 2)

#             # Agregar el puntaje final de asistencia al registro
#             asistencia_por_periodo['puntaje'] = asistencia_por_periodo['porcentaje_asistencia']

#             # Agregar los datos de asistencia del alumno al periodo
#             asistencias_totales.append(asistencia_por_periodo)

#     return jsonify({
#         "profesor_id": profesor.id,
#         "profesor_nombre": profesor.nombre_completo,
#         "materia_id": materia.id,
#         "materia_nombre": materia.nombre,
#         "grado_id": grado_id,
#         "periodo_id": periodo_id if periodo_id else "Todos los periodos",
#         "asistencias": asistencias_totales
#     }), 200




