# app/controllers/alumno_controller.py
from flask import request, jsonify

from traits.bitacora_trait import registrar_bitacora
from datetime import datetime

from models import Alumno, Nota, Asistencia, Participacion, Prediccion, Materia, MateriaProfesor

# Listar todos los alumnos
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

# Ver un solo alumno
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


# Crear alumno
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

# Editar alumno
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

# Eliminar alumno
def eliminar_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    registrar_bitacora('alumno', 'ELIMINAR')
    return jsonify({'message': 'Alumno eliminado'})


 
 
# 1. Perfil

def obtener_perfil_estudiante(alumno_id):
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

# 2. Notas

def obtener_notas_estudiante(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    notas = []
    for n in alumno.notas:
        notas.append({
            "id": n.id,
            "materia_id": n.materia_id,
            "materia_nombre": n.materia.nombre if n.materia else None,
            "periodo_id": n.periodo_id,
            "periodo_nombre": n.periodo.nombre if n.periodo else None,
            "nota_final": n.nota_final,
            "observaciones": n.observaciones
        })
    return jsonify(notas)

# 3. Asistencias

def obtener_asistencias_estudiante(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    asistencias = []
    for a in alumno.asistencias:
        asistencias.append({
            "id": a.id,
            "materia_id": a.materia_id,
            "materia_nombre": a.materia.nombre if a.materia else None,
            "periodo_id": a.periodo_id,
            "periodo_nombre": a.periodo.nombre if a.periodo else None,
            "fecha": a.fecha,
            "presente": a.presente
        })
    return jsonify(asistencias)

# 4. Participaciones

def obtener_participaciones_estudiante(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    participaciones = []
    for p in alumno.participaciones:
        participaciones.append({
            "id": p.id,
            "materia_id": p.materia_id,
            "materia_nombre": p.materia.nombre if p.materia else None,
            "periodo_id": p.periodo_id,
            "periodo_nombre": p.periodo.nombre if p.periodo else None,
            "fecha": p.fecha,
            "puntaje": p.puntaje
        })
    return jsonify(participaciones)

# 5. Predicciones

def obtener_predicciones_estudiante(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    predicciones = []
    for p in alumno.predicciones:
        predicciones.append({
            "id": p.id,
            "periodo_id": p.periodo_id,
            "periodo_nombre": p.periodo.nombre if p.periodo else None,
            "promedio_notas": p.promedio_notas,
            "porcentaje_asistencia": p.porcentaje_asistencia,
            "promedio_participaciones": p.promedio_participaciones,
            "resultado_predicho": p.resultado_predicho
        })
    return jsonify(predicciones)

# 6. Historial (resumen de todo por materia)

def obtener_historial_estudiante(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    historial = []
    for n in alumno.notas:
        historial.append({
            "materia_id": n.materia_id,
            "materia_nombre": n.materia.nombre if n.materia else None,
            "periodo_id": n.periodo_id,
            "periodo_nombre": n.periodo.nombre if n.periodo else None,
            "nota_final": n.nota_final
        })
    return jsonify(historial)

# 7. Materias (las que cursa el alumno por su grado)

def obtener_materias_estudiante(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    materias = []
    for m in alumno.grado.materias:
        materias.append({
            "id": m.id,
            "nombre": m.nombre,
            "turno": m.turno,
            "aula": m.aula,
            "estado": m.estado
        })
    return jsonify(materias)
