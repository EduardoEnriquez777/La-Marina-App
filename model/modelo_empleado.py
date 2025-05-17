from model.modelo_generico import *
from model import Empleado

def obtener_todos_empleados():
    return consultar_todos(Empleado)

def agregar_empleado(data):
    agregar_registro(Empleado, data)

def actualizar_empleado(id_empleado, nuevos_datos):
    return actualizar_registro(Empleado, {'id_empleado': id_empleado}, nuevos_datos)

def eliminar_empleado(id_empleado):
    return eliminar_registro(Empleado, {'id_empleado': id_empleado})
