
from flask import request, jsonify
from datetime import datetime
from traits.bitacora_trait import registrar_bitacora
from models import db
from models import Alumno, nota_bim, Prediccion, Materia, MateriaProfesor
from models.materia import Materia
from models.nota_bim import Nota
from models.periodo import Periodo
from models.alumno_grado import AlumnoGrado
from models.grado import Grado
from models.gestion import Gestion
from models.alumno import Alumno
from models.materia_profesor import MateriaProfesor
from models.alumno_grado import AlumnoGrado
from flask import jsonify
from sqlalchemy.orm import joinedload
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
# ✅ reponde por materai deberia ser por bimestre
def obtener_notas_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)

    # Obtener todas las gestiones en las que estuvo el alumno
    alumno_grados = AlumnoGrado.query \
        .filter_by(alumno_id=alumno_id) \
        .join(Grado).join(Gestion) \
        .options(joinedload(AlumnoGrado.grado).joinedload(Grado.gestion)) \
        .all()

    # Obtener todas las notas
    notas = Nota.query.filter_by(alumno_id=alumno.id).all()

    resultado = {}

    # Registrar todas las gestiones aunque no tengan notas
    for ag in alumno_grados:
        gestion_anio = str(ag.grado.gestion.anio)
        resultado[gestion_anio] = {
            'estado': ag.estado or 'desconocido',
            'notas': []
        }

    # Agregar notas según la gestión
    for nota in notas:
        gestion = nota.grado.gestion.anio if nota.grado and nota.grado.gestion else None
        if gestion:
            gestion_key = str(gestion)
            if gestion_key not in resultado:
                resultado[gestion_key] = {'estado': 'desconocido', 'notas': []}
            resultado[gestion_key]['notas'].append({
                'materia': nota.materia.nombre if nota.materia else "Sin materia",
                'tipo_parcial': nota.tipo_parcial,
                'nota': nota.nota,
                'periodo': nota.periodo.nombre if nota.periodo else "Sin periodo"
            })

    return jsonify(resultado), 200
# ✅
def obtener_asistencias_alumno():
    alumno_id = request.args.get('alumno_id', type=int)
    if not alumno_id:
        return jsonify({"message": "alumno_id es requerido"}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"message": "Alumno no encontrado"}), 404

    # 🟡 Paso 1: Obtener todas las gestiones donde estuvo inscrito el alumno
    alumno_grados = AlumnoGrado.query.filter_by(alumno_id=alumno_id).join(Grado).join(Gestion).all()
    gestiones_del_alumno = {
        ag.grado.gestion.anio: {
            "gestion": ag.grado.gestion.anio,
            "estado": ag.grado.gestion.estado,
            "periodos": {}  # luego llenaremos esto
        }
        for ag in alumno_grados if ag.grado and ag.grado.gestion
    }

    # 🔵 Paso 2: Obtener los datos reales de asistencia
    historial = HistorialAsistenciaParticipacion.query.filter_by(
        alumno_id=alumno_id,
        tipo='asistencia'
    ).all()

    for h in historial:
        grado = Grado.query.get(h.grado_id)
        periodo = Periodo.query.get(h.periodo_id)

        if not grado or not periodo or not grado.gestion:
            continue

        gestion_anio = grado.gestion.anio
        periodo_id = h.periodo_id

        # Inicializar si no existe
        if periodo_id not in gestiones_del_alumno[gestion_anio]["periodos"]:
            gestiones_del_alumno[gestion_anio]["periodos"][periodo_id] = {
                "nombre_periodo": periodo.nombre,
                "nombre_grado": grado.nombre,
                "total_asistencias": 0,
                "total_faltas": 0,
                "total_clases": 0,
                "puntaje": 0.0
            }

        # Sumar asistencia o falta
        if h.puntaje == 100:
            gestiones_del_alumno[gestion_anio]["periodos"][periodo_id]["total_asistencias"] += 1
        else:
            gestiones_del_alumno[gestion_anio]["periodos"][periodo_id]["total_faltas"] += 1

        gestiones_del_alumno[gestion_anio]["periodos"][periodo_id]["total_clases"] += 1

    # 🔶 Paso 3: Calcular puntaje por periodo
    for gestion_data in gestiones_del_alumno.values():
        for periodo_data in gestion_data["periodos"].values():
            total_clases = 40  # o usar periodo_data["total_clases"] si es variable
            if periodo_data["total_clases"] > 0:
                porcentaje = (periodo_data["total_asistencias"] / total_clases) * 100
                periodo_data["puntaje"] = round(porcentaje, 2)

    # 🔴 Paso 4: Convertir resultado al formato deseado
    resultado_final = {
        str(g): {
            "estado": data["estado"],
            "asistencias": list(data["periodos"].values())
        } for g, data in gestiones_del_alumno.items()
    }

    return jsonify({
        "alumno_id": alumno_id,
        "alumno_nombre": alumno.nombre_completo,
        "asistencia_por_gestion": resultado_final
    }), 200
# ✅
def obtener_participacion_alumno():
    alumno_id = request.args.get('alumno_id', type=int)
    
    if not alumno_id:
        return jsonify({"message": "alumno_id es requerido"}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"message": "Alumno no encontrado"}), 404

    # 🟡 Paso 1: Obtener todas las gestiones donde estuvo inscrito el alumno
    alumno_grados = AlumnoGrado.query.filter_by(alumno_id=alumno_id).join(Grado).join(Gestion).all()
    gestiones_del_alumno = {
        ag.grado.gestion.anio: {
            "gestion": ag.grado.gestion.anio,
            "estado": ag.grado.gestion.estado,
            "periodos": {}  # luego llenaremos esto
        }
        for ag in alumno_grados if ag.grado and ag.grado.gestion
    }

    # 🔵 Paso 2: Obtener historial de participación
    historial = HistorialAsistenciaParticipacion.query.filter_by(
        alumno_id=alumno_id,
        tipo='participación'
    ).all()

    for h in historial:
        grado = Grado.query.get(h.grado_id)
        periodo = Periodo.query.get(h.periodo_id)

        if not grado or not periodo or not grado.gestion:
            continue

        gestion_anio = grado.gestion.anio
        periodo_id = h.periodo_id

        # Inicializar si no existe
        if periodo_id not in gestiones_del_alumno[gestion_anio]["periodos"]:
            gestiones_del_alumno[gestion_anio]["periodos"][periodo_id] = {
                "nombre_periodo": periodo.nombre,
                "nombre_grado": grado.nombre,
                "total_participaciones": 0,
                "total_faltas": 0,
                "total_clases": 8,  # Fijo por ahora
                "puntaje": 0.0,
                "porcentaje_participacion": 0.0
            }

        # Sumar participaciones o faltas
        if h.puntaje > 0:
            gestiones_del_alumno[gestion_anio]["periodos"][periodo_id]["total_participaciones"] += 1
            gestiones_del_alumno[gestion_anio]["periodos"][periodo_id]["puntaje"] += h.puntaje
        else:
            gestiones_del_alumno[gestion_anio]["periodos"][periodo_id]["total_faltas"] += 1

    # 🔶 Paso 3: Calcular el porcentaje de participación
    for gestion_data in gestiones_del_alumno.values():
        for periodo_data in gestion_data["periodos"].values():
            total_clases = periodo_data["total_clases"]
            participaciones = periodo_data["total_participaciones"]

            if total_clases > 0:
                porcentaje = (participaciones / total_clases) * 100
                periodo_data["porcentaje_participacion"] = round(porcentaje, 2)

    # 🔴 Paso 4: Convertir resultado final
    resultado_final = {
        str(g): {
            "estado": data["estado"],
            "participaciones": list(data["periodos"].values())
        } for g, data in gestiones_del_alumno.items()
    }

    return jsonify({
        "alumno_id": alumno_id,
        "alumno_nombre": alumno.nombre_completo,
        "participacion_por_gestion": resultado_final
    }), 200
# ✅
def obtener_materias_alumno():
    alumno_id = request.args.get('alumno_id', type=int)
    if not alumno_id:
        return jsonify({"message": "alumno_id es requerido"}), 400

    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return jsonify({"message": "Alumno no encontrado"}), 404

    # Diccionario agrupado por gestión
    materias_por_gestion = {}

    alumno_grados = AlumnoGrado.query.filter_by(alumno_id=alumno_id).all()
    if not alumno_grados:
        return jsonify({"message": "No se encontraron grados para este alumno"}), 404

    for ag in alumno_grados:
        grado = Grado.query.get(ag.grado_id)
        if not grado or not grado.gestion:
            continue

        gestion_anio = grado.gestion.anio
        gestion_estado = grado.gestion.estado

        # Aseguramos la entrada para la gestión
        if gestion_anio not in materias_por_gestion:
            materias_por_gestion[gestion_anio] = {
                'estado': gestion_estado,
                'grados': {}
            }

        # Obtener materias del grado
        materias = Materia.query.filter_by(grado_id=ag.grado_id).all()
        materias_data = [{
            'materia_nombre': m.nombre,
            'materia_codigo': m.codigo
        } for m in materias] if materias else ['No hay materias asignadas para este grado.']

        # Guardar por grado dentro de la gestión
        materias_por_gestion[gestion_anio]['grados'][grado.nombre] = {
            'grado_nombre': grado.nombre,
            'materias': materias_data
        }

    return jsonify({
        "alumno_id": alumno_id,
        "alumno_nombre": alumno.nombre_completo,
        "materias_por_gestion": materias_por_gestion
    }), 200
