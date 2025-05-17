from controllers.controlador_generico import *
from model.modelo_proveedor import Proveedor

COLUMNAS = ['id_proveedor', 'nombre', 'telefono', 'correo', 'direccion']

cargar_proveedores_en_treeview = lambda tree: cargar_datos_en_treeview(tree, Proveedor, COLUMNAS)

guardar_proveedor = lambda data, tree, dialog, es_edicion: guardar_datos(
    Proveedor, data, tree, dialog, claves_pk=['id_proveedor'], es_edicion=es_edicion
)

eliminar_proveedor_seleccionado = lambda tree: eliminar_seleccion(tree, Proveedor, 'id_proveedor')

obtener_datos_de_seleccion = obtener_datos_de_treeview
