from controllers.controlador_generico import *
from model.modelo_almacen import Almacen

COLUMNAS = ['idalmacen', 'nombre', 'ubicacion', 'capacidad_maxima', 'estado']

cargar_almacens_en_treeview = lambda tree: cargar_datos_en_treeview(tree, Almacen, COLUMNAS)

guardar_almacen = lambda data, tree, dialog, es_edicion: guardar_datos(
    Almacen, data, tree, dialog, claves_pk=['idalmacen'], es_edicion=es_edicion
)

eliminar_almacen_seleccionado = lambda tree: eliminar_seleccion(tree, Almacen, 'idalmacen')

obtener_datos_de_seleccion = obtener_datos_de_treeview
