# app/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models import db  # importa todos los modelos automáticamente
from models.inicializar_db import inicializar_db
 
def create_app():
    app = Flask(__name__)

    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/aulainteligente'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'clave_secreta_aula_inteligente'

    # Inicializaciones
    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    with app.app_context():
        inicializar_db()

    # Rutas
    from routes.auth import auth_bp
    from routes.perfil import perfil_bp
    from routes.grado_routes import grado_bp  # si lo tienes
    from routes.profesor_routes import profesor_bp
    from routes.alumno_routes import alumno_bp
    from routes.materia_routes import materia_bp
    from routes.materia_profesor_routes import materia_profesor_bp
    from routes.periodo_routes import periodo_bp
    from routes.nota_routes import nota_bp
    from routes.asistencia_routes import asistencia_bp
    from routes.participacion_routes import participacion_bp
    from routes.tarea_routes import tarea_bp
 
    from routes.prediccion_routes import prediccion_bp
    from routes.bitacora_routes import bitacora_bp
    from routes.rol_routes import rol_bp
    from routes.usuario_routes import usuario_bp
    from routes.observacion_routes import observacion_bp
    from routes.tarea_entregada_routes import tarea_entregada_bp
    from routes.observacion_routes import observacion_bp
    

    app.register_blueprint(auth_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(grado_bp)
    app.register_blueprint(profesor_bp)
    app.register_blueprint(alumno_bp)
    app.register_blueprint(materia_bp)
    app.register_blueprint(materia_profesor_bp)
    app.register_blueprint(periodo_bp)
    app.register_blueprint(nota_bp)
    app.register_blueprint(asistencia_bp)
    app.register_blueprint(participacion_bp)
    app.register_blueprint(tarea_bp)
    
    app.register_blueprint(prediccion_bp)
    app.register_blueprint(bitacora_bp)
    app.register_blueprint(rol_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(tarea_entregada_bp)
    app.register_blueprint(observacion_bp)
    

    @app.route('/')
    def inicio():
        return '🎓 Aula Inteligente backend funcionando'

    return app
