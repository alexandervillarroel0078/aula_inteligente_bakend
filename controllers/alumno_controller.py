
from flask import request, jsonify
from datetime import datetime
from traits.bitacora_trait import registrar_bitacora
from models import db
from models import Alumno, Nota, Asistencia, Participacion, Prediccion, Materia, MateriaProfesor

# CRUD básico
def listar_alumnos():
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
            'grado_id': a.grado_id,
            'grado': {
                'id': a.grado.id if a.grado else None,
                'nombre': a.grado.nombre if a.grado else '-'
            }
        }
        for a in alumnos
    ]
    return jsonify(resultado)

def ver_alumno(id):
    alumno = Alumno.query.get_or_404(id)
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
        'grado_id': alumno.grado_id,
        'grado': {
            'id': alumno.grado.id if alumno.grado else None,
            'nombre': alumno.grado.nombre if alumno.grado else '-'
        }
    })

def crear_alumno():
    data = request.json
    nuevo = Alumno(
        codigo=data['codigo'],
        nombre_completo=data['nombre_completo'],
        fecha_nacimiento=data['fecha_nacimiento'],
        genero=data['genero'],
        email=data['email'],
        telefono=data['telefono'],
        direccion=data['direccion'],
        grado_id=data['grado_id'],
        fecha_registro=datetime.now(),
        estado=data.get('estado', 'activo')
    )
    db.session.add(nuevo)
    db.session.commit()
    registrar_bitacora('alumno', 'CREAR')
    return jsonify({'message': 'Alumno creado exitosamente'})

def editar_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    data = request.json
    alumno.codigo = data['codigo']
    alumno.nombre_completo = data['nombre_completo']
    alumno.fecha_nacimiento = data['fecha_nacimiento']
    alumno.genero = data['genero']
    alumno.email = data['email']
    alumno.telefono = data['telefono']
    alumno.direccion = data['direccion']
    alumno.estado = data['estado']
    alumno.grado_id = data['grado_id']
    db.session.commit()
    registrar_bitacora('alumno', 'EDITAR')
    return jsonify({'message': 'Alumno actualizado'})

def eliminar_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    registrar_bitacora('alumno', 'ELIMINAR')
    return jsonify({'message': 'Alumno eliminado'})

# Funcionalidades para el estudiante
def obtener_perfil_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
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
        "grado_id": alumno.grado_id,
        "grado_nombre": alumno.grado.nombre if alumno.grado else None
    })

def obtener_notas_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    return jsonify([
        {
            "id": n.id,
            "materia_id": n.materia_id,
            "materia_nombre": n.materia.nombre if n.materia else None,
            "periodo_id": n.periodo_id,
            "periodo_nombre": n.periodo.nombre if n.periodo else None,
            "nota_final": n.nota_final,
            "observaciones": n.observaciones
        }
        for n in alumno.notas
    ])

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
    alumno = Alumno.query.get_or_404(alumno_id)
    return jsonify([
        {
            "materia_id": n.materia_id,
            "materia_nombre": n.materia.nombre if n.materia else None,
            "periodo_id": n.periodo_id,
            "periodo_nombre": n.periodo.nombre if n.periodo else None,
            "nota_final": n.nota_final
        }
        for n in alumno.notas
    ])

def obtener_materias_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    return jsonify([
        {
            "id": m.id,
            "nombre": m.nombre,
            "turno": m.turno,
            "aula": m.aula,
            "estado": m.estado
        }
        for m in alumno.grado.materias
    ])




# NO BORRAR
# ✅ Obtener notas por alumno y materia
def obtener_notas_por_materia(alumno_id, materia_id):
    notas = Nota.query.filter_by(alumno_id=alumno_id, materia_id=materia_id).all()
    resultado = []
    for n in notas:
        resultado.append({
            'id': n.id,
            'nota_final': n.nota_final,
            'observaciones': n.observaciones,
            'periodo_id': n.periodo_id,
            'periodo_nombre': n.periodo.nombre if n.periodo else None
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
