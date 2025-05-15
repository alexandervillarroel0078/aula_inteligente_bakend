from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from models.inicializar_db import inicializar_db
from routes.auth import auth_bp

app = Flask(__name__)

# Configuración directa (sin .env)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/aulainteligente'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta_aula_inteligente'

db = SQLAlchemy(app)
CORS(app)

# Inicializa la base de datos (crea tablas y admin)
inicializar_db()

# Rutas
app.register_blueprint(auth_bp)

@app.route('/')
def inicio():
    return '🎓 Aula Inteligente backend funcionando'

if __name__ == '__main__':
    app.run(debug=True)
