import csv
from flask import Flask
from models import db
from models.profesor import Profesor
from models.rol import Rol
from models.gestion import Gestion
from models.grado import Grado
from models.materia import Materia
from models.alumno import Alumno
from models.alumno_grado import AlumnoGrado
from models.materia_profesor import MateriaProfesor
from models.usuario import Usuario
from models.periodo import Periodo
from models.nota_bim import Nota

from models.tarea import Tarea
from models.tarea_entregada import TareaEntregada

from models.observacion import Observacion
from models.prediccion import Prediccion
from models.parcial import Parcial
from models.ponderaciones import Ponderacion
from models.gestion import Gestion
from models.materia_base import MateriaBase
from models.grado_materia import GradoMateria
from models.historial_asistencia_participacion import HistorialAsistenciaParticipacion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/aulainteligente'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def cargar_csv(Modelo, archivo):
    db.session.query(Modelo).delete()
    db.session.commit()

    with open(archivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            clean_row = {}
            for k, v in row.items():
                if v in ("", "null", None):
                    clean_row[k] = None
                elif v.lower() == "true":
                    clean_row[k] = True
                elif v.lower() == "false":
                    clean_row[k] = False
                elif v.isdigit():
                    clean_row[k] = int(v)
                else:
                    try:
                        clean_row[k] = float(v) if '.' in v else v
                    except:
                        clean_row[k] = v
            instancia = Modelo(**clean_row)
            db.session.add(instancia)
        db.session.commit()
        print(f"✅ Datos cargados en: {Modelo.__tablename__}")


with app.app_context():
    # 🔥 1. Eliminar todas las tablas
    db.drop_all()
    print("🧹 Todas las tablas eliminadas")

    # 🧱 2. Crear tablas nuevamente
    db.create_all()
    print("✅ Tablas creadas")

    # 📝 3. Insertar datos desde CSVs
    cargar_csv(Gestion, 'scripts/gestion_utf8.csv')
    cargar_csv(Profesor, 'scripts/profesor_utf8.csv')
    cargar_csv(Rol, 'scripts/rol_utf8.csv')
    cargar_csv(Grado, 'scripts/grado_utf8.csv')
    cargar_csv(Materia, 'scripts/materia_utf8.csv')
    cargar_csv(MateriaBase, 'scripts/materia_base_utf8.csv')
    cargar_csv(GradoMateria, 'scripts/grado_materia_utf8.csv')

    cargar_csv(Alumno, 'scripts/alumno_utf8.csv')
    cargar_csv(AlumnoGrado, 'scripts/alumno_grado_utf8.csv')
    cargar_csv(Usuario, 'scripts/usuario_utf8.csv')
    cargar_csv(MateriaProfesor, 'scripts/materia_profesor_utf8.csv')
    cargar_csv(Periodo, 'scripts/periodo_utf8.csv')
    cargar_csv(Nota, 'scripts/nota_utf8.csv')

    cargar_csv(Tarea, 'scripts/tarea_utf8.csv')
    cargar_csv(TareaEntregada, 'scripts/tarea_entregada_utf8.csv')
    cargar_csv(Parcial,'scripts/parcial_utf8.csv')
    cargar_csv(Observacion, 'scripts/observacion_utf8.csv')
    cargar_csv(Prediccion, 'scripts/prediccion_utf8.csv')
    cargar_csv(Ponderacion, 'scripts/ponderaciones_utf8.csv')
    cargar_csv(HistorialAsistenciaParticipacion, 'scripts/historial_asistencia_participacion_utf8.csv')