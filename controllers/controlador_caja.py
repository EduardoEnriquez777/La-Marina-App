from controllers.controlador_generico import *
from model.modelo_caja import Caja

COLUMNAS = ['idcaja', 'saldo_inicial', 'fecha_apertura', 'saldo_final', 'fecha_cierre']

cargar_cajas_en_treeview = lambda tree: cargar_datos_en_treeview(tree, Caja, COLUMNAS)

guardar_caja = lambda data, tree, dialog, es_edicion: guardar_datos(
    Caja, data, tree, dialog, claves_pk=['idcaja'], es_edicion=es_edicion
)

eliminar_caja_seleccionado = lambda tree: eliminar_seleccion(tree, Caja, 'idcaja')

obtener_datos_de_seleccion = obtener_datos_de_treeview
