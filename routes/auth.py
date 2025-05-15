from flask import Blueprint, request, jsonify, current_app
from config import conectar_db
from werkzeug.security import check_password_hash
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    password = data.get('password')

    if not correo or not password:
        return jsonify({"mensaje": "Correo y contraseña requeridos"}), 400

    conexion = conectar_db()
    if conexion is None:
        return jsonify({"mensaje": "Error de conexión con la base de datos"}), 500

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT u.id, u.nombre, u.correo, u.password, r.nombre
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id
            WHERE u.correo = %s
        """, (correo,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario[3], password):
            payload = {
                'id': usuario[0],
                'nombre': usuario[1],
                'correo': usuario[2],
                'rol': usuario[4],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)
            }

            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                'token': token,
                'usuario': {
                    'id': usuario[0],
                    'nombre': usuario[1],
                    'correo': usuario[2],
                    'rol': usuario[4]
                }
            }), 200
        else:
            return jsonify({"mensaje": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({"mensaje": "Error en el servidor", "error": str(e)}), 500
    finally:
        conexion.close()
