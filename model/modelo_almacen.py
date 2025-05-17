from model.modelo_generico import *
from model import Almacen

def obtener_todos_proveedores():
    return consultar_todos(Almacen)

def agregar_proveedor(data):
    agregar_registro(Almacen, data)

def actualizar_proveedor(id_almacen, nuevos_datos):
    return actualizar_registro(Almacen, {'idalmacen': id_almacen}, nuevos_datos)

def eliminar_proveedor(id_almacen):
    return eliminar_registro(Almacen, {'idalmacen': id_almacen})
