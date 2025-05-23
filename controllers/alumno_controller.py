# app/controllers/alumno_controller.py
from flask import request, jsonify
from models import db, Alumno
from traits.bitacora_trait import registrar_bitacora
from datetime import datetime

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
            'grado_id': a.grado_id
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
        'grado_id': alumno.grado_id
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
