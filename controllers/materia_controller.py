from flask import jsonify, request
from models import db
from models.materia import Materia
from models.materia import Materia
from models.alumno_grado import AlumnoGrado
from models.alumno import Alumno
from models.gestion import Gestion  
from models.grado import Grado
from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion
from traits.bitacora_trait import registrar_bitacora

def listar_materias():
    gestiones = Gestion.query.order_by(Gestion.anio).all()
    resultado = []

    for gestion in gestiones:
        grados = Grado.query.filter_by(gestion_id=gestion.id).order_by(Grado.nombre).all()
        grados_data = []

        for grado in grados:
            materias = Materia.query.filter_by(grado_id=grado.id).all()
            materias_data = [{
                "id": m.id,
                "nombre": m.nombre,
                "codigo": m.codigo,
                "aula": m.aula,
                "turno": m.turno,
                "estado": m.estado
            } for m in materias]

            grados_data.append({
                "id": grado.id,
                "nombre": grado.nombre,
                "materias": materias_data
            })

        resultado.append({
            "gestion": gestion.anio,
            "estado": gestion.estado,
            "grados": grados_data
        })

    return jsonify(resultado), 200






def ver_materia(id):
    m = Materia.query.get_or_404(id)
    return jsonify({
        "id": m.id,
        "codigo": m.codigo,
        "nombre": m.nombre,
        "descripcion": m.descripcion,
        "turno": m.turno,
        "aula": m.aula,
        "estado": m.estado,
        "grado_id": m.grado_id
    })

def crear_materia(request):
    data = request.get_json()
    nueva = Materia(
        codigo=data['codigo'],
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        turno=data['turno'],
        aula=data['aula'],
        estado=data['estado'],
        grado_id=data['grado_id']
    )
    db.session.add(nueva)
    db.session.commit()
    registrar_bitacora("materia", f"creó materia ID {nueva.id}")
    return jsonify({"mensaje": "Materia registrada correctamente", "id": nueva.id})

def editar_materia(id, request):
    m = Materia.query.get_or_404(id)
    data = request.get_json()
    m.codigo = data['codigo']
    m.nombre = data['nombre']
    m.descripcion = data.get('descripcion')
    m.turno = data['turno']
    m.aula = data['aula']
    m.estado = data['estado']
    m.grado_id = data['grado_id']

    db.session.commit()
    registrar_bitacora("materia", f"editó materia ID {id}")
    return jsonify({"mensaje": "Materia actualizada correctamente"})

def eliminar_materia(id):
    m = Materia.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    registrar_bitacora("materia", f"eliminó materia ID {id}")
    return jsonify({"mensaje": "Materia eliminada correctamente"})

def listar_alumnos_por_materia(materia_id):
    materia = Materia.query.get_or_404(materia_id)

    alumnos = (
        db.session.query(Alumno)
        .join(AlumnoGrado, Alumno.id == AlumnoGrado.alumno_id)
        .filter(AlumnoGrado.grado_id == materia.grado_id)
        .all()
    )

    resultado = [{
        "id": alumno.id,
        "codigo": alumno.codigo,
        "nombre_completo": alumno.nombre_completo,
        "estado": alumno.estado
    } for alumno in alumnos]

    return jsonify({
        "total": len(resultado),
        "estudiantes": resultado
    }), 200



 
def obtener_asistencias_de_alumno():
    alumno_id = request.args.get('alumno_id', type=int)
    gestion = request.args.get('gestion', type=int)
    materia_id = request.args.get('materia_id', type=int)
    periodo_id = request.args.get('periodo_id', type=int)

    if not alumno_id or not gestion or not materia_id or not periodo_id:
        return jsonify({"message": "Faltan parámetros requeridos"}), 400

    asistencias = HistorialAsistenciaParticipacion.query.filter_by(
        alumno_id=alumno_id,
        gestion=gestion,
        materia_id=materia_id,
        periodo_id=periodo_id,
        tipo='asistencia'
    ).order_by(HistorialAsistenciaParticipacion.fecha.asc()).all()

    resultados = [
        {
            "fecha": a.fecha,
            "puntaje": a.puntaje,
            "observaciones": a.observaciones
        }
        for a in asistencias
    ]

    return jsonify({
        "alumno_id": alumno_id,
        "asistencias": resultados
    }), 200