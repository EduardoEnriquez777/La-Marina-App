from conexion import get_db

try:
    db = next(get_db())
    print("✅ ¡Conexión exitosa a la base de datos!")
except Exception as e:
    print("❌ Error al conectar:", e)   