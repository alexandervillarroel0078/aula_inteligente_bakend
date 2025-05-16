from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# IMPORTA TODOS LOS MODELOS AQUÍ
from .alumno import Alumno
from .grado import Grado
from .materia import Materia
from .profesor import Profesor
from .materia_profesor import MateriaProfesor
from .usuario import Usuario
from .rol import Rol
from .configuracion import Configuracion
from .periodo import Periodo
from .nota import Nota
from .asistencia import Asistencia
from .participacion import Participacion
from .tarea import Tarea
from .entrega_tarea import EntregaTarea
from .observacion import Observacion
from .bitacora import Bitacora
from .prediccion import Prediccion
