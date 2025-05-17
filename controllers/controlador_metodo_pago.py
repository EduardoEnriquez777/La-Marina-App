from controllers.controlador_generico import *
from model.modelo_metodo_pago import MetodoPago

COLUMNAS = ['idmetodo_pago', 'nombre', 'descripcion', 'activo']

cargar_metodo_pago_en_treeview = lambda tree: cargar_datos_en_treeview(tree, MetodoPago, COLUMNAS)

guardar_metodo_pago = lambda data, tree, dialog, es_edicion: guardar_datos(
    MetodoPago, data, tree, dialog, claves_pk=['idmetodo_pago'], es_edicion=es_edicion
)

eliminar_metodo_pago_seleccionado = lambda tree: eliminar_seleccion(tree, MetodoPago, 'idmetodo_pago')

obtener_datos_de_seleccion = obtener_datos_de_treeview
