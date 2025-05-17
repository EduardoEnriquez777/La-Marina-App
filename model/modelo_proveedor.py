from model.modelo_generico import *
from model import Proveedor

def obtener_todos_proveedores():
    return consultar_todos(Proveedor)

def agregar_proveedor(data):
    agregar_registro(Proveedor, data)

def actualizar_proveedor(id_proveedor, nuevos_datos):
    return actualizar_registro(Proveedor, {'id_proveedor': id_proveedor}, nuevos_datos)

def eliminar_proveedor(id_proveedor):
    return eliminar_registro(Proveedor, {'id_proveedor': id_proveedor})
