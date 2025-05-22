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

    app.register_blueprint(auth_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(grado_bp)
    app.register_blueprint(profesor_bp)
    app.register_blueprint(alumno_bp)
    @app.route('/')
    def inicio():
        return '🎓 Aula Inteligente backend funcionando'

    return app
