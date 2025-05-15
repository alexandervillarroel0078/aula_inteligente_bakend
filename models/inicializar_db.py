from config import conectar_db
from werkzeug.security import generate_password_hash

def crear_tabla_roles():
    conexion = conectar_db()
    if conexion is None:
        print("❌ No se pudo conectar para crear tabla roles.")
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(50) UNIQUE NOT NULL
            );
        """)
        conexion.commit()
        print("✅ Tabla 'roles' creada o existente.")
    except Exception as e:
        print("❌ Error al crear tabla roles:", e)
    finally:
        conexion.close()

def crear_tabla_usuarios():
    conexion = conectar_db()
    if conexion is None:
        print("❌ No se pudo conectar para crear tabla usuarios.")
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                id_rol INTEGER REFERENCES roles(id)
            );
        """)
        conexion.commit()
        print("✅ Tabla 'usuarios' creada o existente.")
    except Exception as e:
        print("❌ Error al crear tabla usuarios:", e)
    finally:
        conexion.close()

def insertar_roles():
    conexion = conectar_db()
    if conexion is None:
        print("❌ No se pudo conectar para insertar roles.")
        return

    try:
        cursor = conexion.cursor()
        roles = ['admin', 'docente', 'estudiante']
        for rol in roles:
            cursor.execute("""
                INSERT INTO roles (nombre)
                VALUES (%s)
                ON CONFLICT (nombre) DO NOTHING
            """, (rol,))
        conexion.commit()
        print("✅ Roles básicos insertados.")
    except Exception as e:
        print("❌ Error al insertar roles:", e)
    finally:
        conexion.close()

def crear_usuario_admin():
    conexion = conectar_db()
    if conexion is None:
        print("❌ No se pudo conectar para crear usuario admin.")
        return

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE correo = 'admin@admin.com'")
        if cursor.fetchone():
            print("ℹ️ Usuario admin ya existe.")
            return

        cursor.execute("SELECT id FROM roles WHERE nombre = 'admin'")
        rol_admin = cursor.fetchone()
        if not rol_admin:
            print("❌ Rol admin no encontrado.")
            return

        password_hash = generate_password_hash('123456')
        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, password, id_rol)
            VALUES (%s, %s, %s, %s)
        """, ('Admin', 'admin@admin.com', password_hash, rol_admin[0]))
        conexion.commit()
        print("✅ Usuario admin creado: admin@admin.com / 123456")
    except Exception as e:
        print("❌ Error al crear usuario admin:", e)
    finally:
        conexion.close()

def inicializar_db():
    print("🔧 Iniciando creación de tablas...")
    crear_tabla_roles()
    crear_tabla_usuarios()
    insertar_roles()
    crear_usuario_admin()
    print("✅ Base de datos lista.")
