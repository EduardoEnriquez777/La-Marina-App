from model.modelo_generico import *
from model import Caja

def obtener_todos_cajas():
    return consultar_todos(Caja)

def agregar_caja(data):
    agregar_registro(Caja, data)

def actualizar_caja(idcaja, nuevos_datos):
    return actualizar_registro(Caja, {'idcaja': idcaja}, nuevos_datos)

def eliminar_caja(idcaja):
    return eliminar_registro(Caja, {'idcaja': idcaja})
