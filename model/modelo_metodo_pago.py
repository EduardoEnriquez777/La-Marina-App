from model.modelo_generico import *
from model import MetodoPago

def obtener_todos_metodo_pagos():
    return consultar_todos(MetodoPago)

def agregar_cliente(data):
    agregar_registro(MetodoPago, data)

def actualizar_cliente(idmetodo_pago, nuevos_datos):
    return actualizar_registro(MetodoPago, {'idmetodo_pago': idmetodo_pago}, nuevos_datos)

def eliminar_cliente(idmetodo_pago):
    return eliminar_registro(MetodoPago, {'idmetodo_pago': idmetodo_pago})
