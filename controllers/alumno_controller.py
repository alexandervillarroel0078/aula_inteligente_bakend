
from flask import request, jsonify
from datetime import datetime
from traits.bitacora_trait import registrar_bitacora
from models import db
from models import Alumno, Nota, Asistencia, Participacion, Prediccion, Materia, MateriaProfesor
from models.materia import Materia
from models.nota import Nota
from models.periodo import Periodo
from flask import jsonify, abort

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
    
    # Verificar si falta algún periodo (bimestre) en los resultados
    periodos_existentes = [n.periodo_id for n in notas]
    todos_los_periodos = [1, 2, 3, 4]  # Los IDs de los bimestres

    # Verificar si algún periodo falta
    for periodo in todos_los_periodos:
        if periodo not in periodos_existentes:
            # Agregar el bimestre que falta
            resultado.append({
                'id': None,
                'nota_final': None,
                'observaciones': None,
                'periodo_id': periodo,
                'periodo_nombre': f'{periodo}er Bimestre' if periodo == 1 else f'{periodo}do Bimestre' if periodo == 2 else f'{periodo}er Bimestre' if periodo == 3 else f'{periodo}to Bimestre'
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
