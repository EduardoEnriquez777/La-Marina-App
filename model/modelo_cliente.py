from model.modelo_generico import *
from model import Cliente

def obtener_todos_clientes():
    return consultar_todos(Cliente)

def agregar_cliente(data):
    agregar_registro(Cliente, data)

def actualizar_cliente(idcliente, nuevos_datos):
    return actualizar_registro(Cliente, {'id_cliente': idcliente}, nuevos_datos)

def eliminar_cliente(idcliente):
    return eliminar_registro(Cliente, {'id_cliente': idcliente})
