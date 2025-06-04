from flask import jsonify
from models import db
from models.prediccion import Prediccion
from models.nota_trimestre import NotaTrimestre
from models.alumno import Alumno
from models.alumno_grado import AlumnoGrado
from models.materia_profesor import MateriaProfesor
import numpy as np
import joblib

# modelo = joblib.load('modelo_lineal.pkl')
import os

ruta_modelo = os.path.join(os.path.dirname(__file__), '..', 'modelo_lineal.pkl')
modelo = joblib.load(ruta_modelo)

def clasificar_rendimiento(valor):
    if valor < 60:
        return "Bajo"
    elif valor < 80:
        return "Medio"
    else:
        return "Alto"



def generar_predicciones_por_profesor_grado_periodo(profesor_id, grado_id, periodo_id):
    materias_asignadas = MateriaProfesor.query.filter_by(
        profesor_id=profesor_id,
        grado_id=grado_id
    ).all()

    alumnos = Alumno.query\
        .join(AlumnoGrado)\
        .filter(AlumnoGrado.grado_id == grado_id)\
        .all()

    resumen = {}

    def obtener_semestre(periodo_id):
        if periodo_id == 1:
            return "Primer Trimestre"
        elif periodo_id == 2:
            return "Segundo Trimestre"
        elif periodo_id == 3:
            return "Tercer Trimestre"
        else:
            return f"Periodo {periodo_id}"

    semestre_actual = obtener_semestre(periodo_id)
    semestre_siguiente = obtener_semestre(periodo_id + 1)

    for mp in materias_asignadas:
        materia_id = mp.materia_id
        materia_nombre = mp.materia.nombre
        resumen[materia_nombre] = []

        for alumno in alumnos:
            nota_trimestre = NotaTrimestre.query.filter_by(
                alumno_id=alumno.id,
                materia_id=materia_id,
                periodo_id=periodo_id
            ).first()

            if not nota_trimestre:
                continue

            nota = nota_trimestre.nota_parcial or 0
            asistencia = nota_trimestre.asistencia_trimestre or 0
            participacion = nota_trimestre.participacion_trimestre or 0

            entrada = np.array([[nota, asistencia, participacion]])
            predicho = modelo.predict(entrada)[0]
            clasificacion = clasificar_rendimiento(predicho)

            prediccion = Prediccion.query.filter_by(
                alumno_id=alumno.id,
                materia_id=materia_id,
                periodo_id=periodo_id + 1
            ).first()

            if prediccion:
                prediccion.nota_parcial = nota
                prediccion.asistencia = asistencia
                prediccion.participacion = participacion
                prediccion.rendimiento_predicho = float(predicho)
                prediccion.clasificacion = clasificacion
            else:
                prediccion = Prediccion(
                    alumno_id=alumno.id,
                    materia_id=materia_id,
                    periodo_id=periodo_id + 1,
                    nota_parcial=nota,
                    asistencia=asistencia,
                    participacion=participacion,
                    rendimiento_predicho=float(predicho),
                    clasificacion=clasificacion
                )
                db.session.add(prediccion)

            resumen[materia_nombre].append({
                "alumno_id": alumno.id,
                "alumno": f"{alumno.nombre} {alumno.apellido}",
                "nota": nota,
                "asistencia": asistencia,
                "participacion": participacion,
                "prediccion": round(predicho, 2),
                "clasificacion": clasificacion
            })

    db.session.commit()

    return jsonify({
        "mensaje": f"Predicciones generadas para el {semestre_siguiente} del profesor {profesor_id} en grado {grado_id} y periodo {semestre_actual}.",
        "resumen": resumen
    })

def hacer_prediccion_y_guardar(alumno_id, materia_id, periodo_id, nota_parcial, asistencia, participacion):
    entrada = np.array([[nota_parcial, asistencia, participacion]])
    predicho = modelo.predict(entrada)[0]
    clasificacion = clasificar_rendimiento(predicho)

    prediccion = Prediccion.query.filter_by(
        alumno_id=alumno_id,
        materia_id=materia_id,
        periodo_id=periodo_id
    ).first()

    if prediccion:
        # Actualizar si ya existe
        prediccion.nota_parcial = nota_parcial
        prediccion.asistencia = asistencia
        prediccion.participacion = participacion
        prediccion.rendimiento_predicho = float(predicho)
        prediccion.clasificacion = clasificacion
    else:
        # Crear si no existe
        prediccion = Prediccion(
            alumno_id=alumno_id,
            materia_id=materia_id,
            periodo_id=periodo_id,
            nota_parcial=nota_parcial,
            asistencia=asistencia,
            participacion=participacion,
            rendimiento_predicho=float(predicho),
            clasificacion=clasificacion
        )
        db.session.add(prediccion)

    db.session.commit()

    return jsonify({
        "alumno_id": alumno_id,
        "materia_id": materia_id,
        "periodo_id": periodo_id,
        "rendimiento_predicho": round(predicho, 2),
        "clasificacion": clasificacion
    })

def generar_predicciones_para_todos(grado_id, materia_id, periodo_id):
    alumnos = Alumno.query\
        .join(AlumnoGrado)\
        .filter(AlumnoGrado.grado_id == grado_id)\
        .all()

    predicciones_creadas = []

    for alumno in alumnos:
        nota_trimestre = NotaTrimestre.query.filter_by(
            alumno_id=alumno.id,
            materia_id=materia_id,
            periodo_id=periodo_id
        ).first()

        if not nota_trimestre:
            continue

        nota = nota_trimestre.nota_parcial or 0
        asistencia = nota_trimestre.asistencia_trimestre or 0
        participacion = nota_trimestre.participacion_trimestre or 0

        entrada = np.array([[nota, asistencia, participacion]])
        predicho = modelo.predict(entrada)[0]
        clasificacion = clasificar_rendimiento(predicho)

        prediccion = Prediccion.query.filter_by(
            alumno_id=alumno.id,
            materia_id=materia_id,
            periodo_id=periodo_id
        ).first()

        if prediccion:
            prediccion.nota_parcial = nota
            prediccion.asistencia = asistencia
            prediccion.participacion = participacion
            prediccion.rendimiento_predicho = float(predicho)
            prediccion.clasificacion = clasificacion
        else:
            prediccion = Prediccion(
                alumno_id=alumno.id,
                materia_id=materia_id,
                periodo_id=periodo_id,
                nota_parcial=nota,
                asistencia=asistencia,
                participacion=participacion,
                rendimiento_predicho=float(predicho),
                clasificacion=clasificacion
            )
            db.session.add(prediccion)

        predicciones_creadas.append(alumno.id)

    db.session.commit()

    return jsonify({
        "mensaje": f"Predicciones generadas para {len(predicciones_creadas)} alumnos.",
        "alumnos": predicciones_creadas
    })



def listar_todas_las_predicciones():
    predicciones = Prediccion.query.all()
    resultado = []
    for p in predicciones:
        resultado.append({
            'id': p.id,
            'alumno_id': p.alumno_id,
            'alumno': p.alumno.nombre,
            'materia_id': p.materia_id,
            'materia': p.materia.nombre,
            'periodo_id': p.periodo_id,
            'periodo': p.periodo.nombre,
            'nota_parcial': p.nota_parcial,
            'asistencia': p.asistencia,
            'participacion': p.participacion,
            'rendimiento_predicho': p.rendimiento_predicho,
            'clasificacion': p.clasificacion
        })
    return jsonify(resultado)

def predicciones_por_alumno(alumno_id):
    predicciones = Prediccion.query.filter_by(alumno_id=alumno_id).all()
    resultado = []
    for p in predicciones:
        resultado.append({
            'materia': p.materia.nombre,
            'periodo': p.periodo.nombre,
            'nota_parcial': p.nota_parcial,
            'asistencia': p.asistencia,
            'participacion': p.participacion,
            'rendimiento_predicho': p.rendimiento_predicho,
            'clasificacion': p.clasificacion
        })
    return jsonify(resultado)
