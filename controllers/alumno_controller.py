
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

# Crear un nuevo alumno
def crear_alumno():
    data = request.json
    
    # Crear el nuevo alumno
    nuevo = Alumno(
        codigo=data['codigo'],
        nombre_completo=data['nombre_completo'],
        fecha_nacimiento=data['fecha_nacimiento'],
        genero=data['genero'],
        email=data['email'],
        telefono=data['telefono'],
        direccion=data['direccion'],
        fecha_registro=datetime.now(),
        estado=data.get('estado', 'activo')
    )
    
    # Añadir el nuevo alumno a la sesión
    db.session.add(nuevo)
    db.session.commit()
    
    # Crear la relación en la tabla 'alumno_grado'
    if 'grado_id' in data:
        alumno_grado = AlumnoGrado(
            alumno_id=nuevo.id,
            grado_id=data['grado_id'],
            gestion=data.get('gestion', 2024),
        )
        db.session.add(alumno_grado)
        db.session.commit()
    
    # Registrar en la bitácora
    registrar_bitacora('alumno', 'CREAR')
    
    return jsonify({'message': 'Alumno creado exitosamente'})

# Editar un alumno existente
def editar_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    data = request.json
    
    # Actualizar los campos del alumno
    alumno.codigo = data['codigo']
    alumno.nombre_completo = data['nombre_completo']
    alumno.fecha_nacimiento = data['fecha_nacimiento']
    alumno.genero = data['genero']
    alumno.email = data['email']
    alumno.telefono = data['telefono']
    alumno.direccion = data['direccion']
    alumno.estado = data['estado']
    
    # Actualizar la relación con 'alumno_grado' (si es necesario)
    if 'grado_id' in data:
        # Eliminar la relación existente en caso de que el grado haya cambiado
        AlumnoGrado.query.filter_by(alumno_id=alumno.id).delete()
        db.session.commit()
        
        # Crear la nueva relación en 'alumno_grado'
        alumno_grado = AlumnoGrado(
            alumno_id=alumno.id,
            grado_id=data['grado_id'],
            gestion=data.get('gestion', 2024),
        )
        db.session.add(alumno_grado)
        db.session.commit()
    
    db.session.commit()
    
    # Registrar en la bitácora
    registrar_bitacora('alumno', 'EDITAR')
    
    return jsonify({'message': 'Alumno actualizado exitosamente'})

# Eliminar un alumno
def eliminar_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    
    # Eliminar las relaciones en la tabla 'alumno_grado'
    AlumnoGrado.query.filter_by(alumno_id=alumno.id).delete()
    
    # Eliminar el alumno
    db.session.delete(alumno)
    db.session.commit()
    
    # Registrar en la bitácora
    registrar_bitacora('alumno', 'ELIMINAR')
    
    return jsonify({'message': 'Alumno eliminado exitosamente'})

# Funcionalidades para el estudiante
def obtener_perfil_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    
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
        "grados": grados  # Los grados asociados al alumno
    })

def obtener_notas_alumno(alumno_id):
    # Obtener el alumno o lanzar un error 404 si no existe
    alumno = Alumno.query.get_or_404(alumno_id)

    # Obtener todas las notas del alumno
    notas = Nota.query.filter_by(alumno_id=alumno.id).all()

    # Construir la respuesta en formato JSON
    resultado = []
    for nota in notas:
        resultado.append({
            'id': nota.id,
            'materia_id': nota.materia_id,
            'materia_nombre': nota.materia.nombre if nota.materia else None,
            'periodo_id': nota.periodo_id,
            'periodo_nombre': nota.periodo.nombre if nota.periodo else None,
            'nota_final': nota.nota,
            'observaciones': nota.observaciones,
            'tipo_parcial': nota.tipo_parcial  # Agregado para el tipo de parcial
        })

    # Devolver los resultados como JSON
    return jsonify(resultado)


def obtener_asistencias_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    return jsonify([
        {
            "id": a.id,
            "materia_id": a.materia_id,
            "materia_nombre": a.materia.nombre if a.materia else None,
            "periodo_id": a.periodo_id,
            "periodo_nombre": a.periodo.nombre if a.periodo else None,
            "fecha": a.fecha,
            "presente": a.presente
        }
        for a in alumno.asistencias
    ])

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


def obtener_materias_alumno(alumno_id):
    # Obtener el alumno o lanzar un error 404 si no existe
    alumno = Alumno.query.get_or_404(alumno_id)

    # Obtener los grados a los que está asignado el alumno
    grados = AlumnoGrado.query.filter_by(alumno_id=alumno.id).all()

    # Lista para almacenar las materias de cada grado
    materias = []

    # Iterar sobre los grados y obtener las materias relacionadas
    for grado in grados:
        # Obtener el grado
        grado_obj = Grado.query.get(grado.grado_id)

        # Obtener las materias asociadas con ese grado
        for materia in grado_obj.materias:
            materias.append({
                'materia_id': materia.id,
                'materia_nombre': materia.nombre,
                'grado_id': grado.grado_id,
                'grado_nombre': grado_obj.nombre,
                'turno': grado_obj.turno,  # Obtener el turno de la materia
            })
    
    # Devolver las materias del alumno como respuesta en formato JSON
    return jsonify(materias)

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


