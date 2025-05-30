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
from .nota_bim import Nota
from .tarea import Tarea
from .tarea_entregada import TareaEntregada

from .observacion import Observacion
from .bitacora import Bitacora
from .prediccion import Prediccion
from .alumno_grado import AlumnoGrado
from .parcial import Parcial