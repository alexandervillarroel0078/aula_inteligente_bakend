from flask import Blueprint, request, jsonify, current_app
from config import conectar_db
from werkzeug.security import check_password_hash
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    password = data.get('password')

    if not nombre_usuario or not password:
        return jsonify({"mensaje": "Usuario y contraseña requeridos"}), 400

    conexion = conectar_db()
    if conexion is None:
        return jsonify({"mensaje": "Error de conexión con la base de datos"}), 500

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT u.id, u.nombre_usuario, u.password_hash, r.nombre
            FROM usuario u
            JOIN rol r ON u.rol_id = r.id
            WHERE u.nombre_usuario = %s
        """, (nombre_usuario,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario[2], password):
            payload = {
    'id': usuario[0],
    'nombre_usuario': usuario[1],  # antes estaba como 'nombre'
    'correo': usuario[2],
    'rol': usuario[3],
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)
}


            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                'token': token,
                'usuario': {
                    'id': usuario[0],
                    'nombre_usuario': usuario[1],
                    'correo': usuario[2],
                    'rol': usuario[3]
                }
            }), 200
        else:
            return jsonify({"mensaje": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({"mensaje": "Error en el servidor", "error": str(e)}), 500
    finally:
        conexion.close()
