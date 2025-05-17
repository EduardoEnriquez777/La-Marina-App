from model.modelo_generico import *
from model import Sucursal

def obtener_todos_sucursal():
    return consultar_todos(Sucursal)

def agregar_sucursal(data):
    agregar_registro(Sucursal, data)

def actualizar_sucursal(id_sucursal, nuevos_datos):
    return actualizar_registro(Sucursal, {'id_sucursal': id_sucursal}, nuevos_datos)

def eliminar_sucursal(id_sucursal):
    return eliminar_registro(Sucursal, {'id_sucursal': id_sucursal})
