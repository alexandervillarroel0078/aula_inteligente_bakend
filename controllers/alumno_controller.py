from flask import jsonify
from models import db
from models.alumno import Alumno

def listar_alumnos():
    alumnos = Alumno.query.all()
    return jsonify([
        {
            "id": a.id,
            "nombre_completo": a.nombre_completo,
            "fecha_nacimiento": str(a.fecha_nacimiento),
            "genero": a.genero,
            "email": a.email,
            "telefono": a.telefono,
            "direccion": a.direccion,
            "grado_id": a.grado_id,
            "grado_nombre": a.grado.nombre if a.grado else None,  # ← añadido
            "fecha_registro": str(a.fecha_registro) if a.fecha_registro else None,
            "estado": a.estado
        } for a in alumnos
    ])

def obtener_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    return jsonify({
        "id": alumno.id,
        "nombre_completo": alumno.nombre_completo,
        "fecha_nacimiento": str(alumno.fecha_nacimiento),
        "genero": alumno.genero,
        "email": alumno.email,
        "telefono": alumno.telefono,
        "direccion": alumno.direccion,
        "grado_id": alumno.grado_id,
        "grado_nombre": alumno.grado.nombre if alumno.grado else None,  # ← añadido
        "fecha_registro": str(alumno.fecha_registro) if alumno.fecha_registro else None,
        "estado": alumno.estado
    })

def crear_alumno(request):
    data = request.get_json()
    nuevo = Alumno(
        nombre_completo=data.get('nombre_completo'),
        fecha_nacimiento=data.get('fecha_nacimiento'),
        genero=data.get('genero'),
        email=data.get('email'),
        telefono=data.get('telefono'),
        direccion=data.get('direccion'),
        grado_id=data.get('grado_id'),
        fecha_registro=data.get('fecha_registro'),
        estado=data.get('estado')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Alumno creado con éxito"}), 201

def actualizar_alumno(id, request):
    alumno = Alumno.query.get_or_404(id)
    data = request.get_json()

    alumno.nombre_completo = data.get('nombre_completo', alumno.nombre_completo)
    alumno.fecha_nacimiento = data.get('fecha_nacimiento', alumno.fecha_nacimiento)
    alumno.genero = data.get('genero', alumno.genero)
    alumno.email = data.get('email', alumno.email)
    alumno.telefono = data.get('telefono', alumno.telefono)
    alumno.direccion = data.get('direccion', alumno.direccion)
    alumno.grado_id = data.get('grado_id', alumno.grado_id)
    alumno.fecha_registro = data.get('fecha_registro', alumno.fecha_registro)
    alumno.estado = data.get('estado', alumno.estado)

    db.session.commit()
    return jsonify({"mensaje": "Alumno actualizado con éxito"})

def eliminar_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    return jsonify({"mensaje": "Alumno eliminado con éxito"})
