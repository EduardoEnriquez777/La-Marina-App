from controllers.controlador_generico import *
from model.modelo_sucursal import Sucursal

COLUMNAS = ['id_sucursal', 'nombre', 'direccion', 'ciudad', 'estado', 'codigo_postal', 'telefono']

cargar_sucursals_en_treeview = lambda tree: cargar_datos_en_treeview(tree, Sucursal, COLUMNAS)

guardar_sucursal = lambda data, tree, dialog, es_edicion: guardar_datos(
    Sucursal, data, tree, dialog, claves_pk=['id_sucursal'], es_edicion=es_edicion
)

eliminar_sucursal_seleccionado = lambda tree: eliminar_seleccion(tree, Sucursal, 'id_sucursal')

obtener_datos_de_seleccion = obtener_datos_de_treeview


def obtener_sucursales_disponibles():
    sucursales = ("sucursal")  # Asumiendo que este retorna una lista de diccionarios
    return [str(s["id_sucursal"]) for s in sucursales]
