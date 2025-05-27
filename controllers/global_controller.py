from flask import jsonify, request
from models import db
from models.alumno import Alumno
from models.periodo import Periodo
from models.grado import Grado
from models.materia import Materia
from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion  # Importamos el modelo

# Listar historial de asistencia y participación
def listar_historial():
    # Obtener todos los registros de asistencia o participación
    historial = HistorialAsistenciaParticipacion.query.all()
    
    # Devolver la lista de historiales como JSON
    return jsonify([{
        "id": h.id,
        "alumno_id": h.alumno_id,
        "materia_id": h.materia_id,
        "periodo_id": h.periodo_id,
        "grado_id": h.grado_id,
        "gestion": h.gestion,
        "tipo": h.tipo,  # 'asistencia' o 'participacion'
        "puntaje": h.puntaje,
        "fecha": str(h.fecha),
        "observaciones": h.observaciones
    } for h in historial])





from flask import jsonify, request
from models import db
from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion  # Importamos el modelo

# Filtrar historial por múltiples parámetros: tipo, gestión, materia, periodo, alumno, grado
def filtrar_historial():
    tipo = request.args.get('tipo', '')  # 'asistencia' o 'participacion'
    gestion = request.args.get('gestion', type=int)  # Año de la gestión
    materia_id = request.args.get('materia_id', type=int)  # ID de la materia (opcional)
    periodo_id = request.args.get('periodo_id', type=int)  # ID del periodo (opcional)
    alumno_id = request.args.get('alumno_id', type=int)  # ID del alumno (opcional)
    grado_id = request.args.get('grado_id', type=int)  # ID del grado (opcional)

    # Construir la consulta base
    query = HistorialAsistenciaParticipacion.query

    # Filtrar por tipo si se pasa
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    # Filtrar por gestión si se pasa
    if gestion:
        query = query.filter_by(gestion=gestion)

    # Filtrar por materia_id si se pasa
    if materia_id:
        query = query.filter_by(materia_id=materia_id)

    # Filtrar por periodo_id si se pasa
    if periodo_id:
        query = query.filter_by(periodo_id=periodo_id)

    # Filtrar por alumno_id si se pasa
    if alumno_id:
        query = query.filter_by(alumno_id=alumno_id)

    # Filtrar por grado_id si se pasa
    if grado_id:
        query = query.filter_by(grado_id=grado_id)

    # Ejecutar la consulta
    historial = query.all()

    # Verificar si hay registros
    if historial:
        # Devolver los registros filtrados como JSON
        resultado = []
        for h in historial:
            # Obtener los nombres de los id relacionados
            alumno = Alumno.query.get(h.alumno_id)
            materia = Materia.query.get(h.materia_id)
            grado = Grado.query.get(h.grado_id)
            periodo = Periodo.query.get(h.periodo_id)

            resultado.append({
                "id": h.id,
                "alumno_id": h.alumno_id,
                "alumno_nombre": alumno.nombre_completo if alumno else "Desconocido",  # Nombre del alumno
                "materia_id": h.materia_id,
                "materia_nombre": materia.nombre if materia else "Desconocida",  # Nombre de la materia
                "periodo_id": h.periodo_id,
                "periodo_nombre": periodo.nombre if periodo else "Desconocido",  # Nombre del periodo
                "grado_id": h.grado_id,
                "grado_nombre": grado.nombre if grado else "Desconocido",  # Nombre del grado
                "gestion": h.gestion,
                "tipo": h.tipo,  # 'asistencia' o 'participacion'
                "puntaje": h.puntaje,
                "fecha": str(h.fecha),
                "observaciones": h.observaciones
            })

        return jsonify(resultado), 200
    else:
        return jsonify({"message": "No se encontraron registros con esos parámetros"}), 404


