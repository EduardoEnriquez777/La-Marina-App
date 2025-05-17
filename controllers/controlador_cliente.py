from controllers.controlador_generico import *
from model.modelo_cliente import Cliente

COLUMNAS = ['id_cliente', 'nombre', 'apellido', 'telefono', 'correo', 'direccion']

cargar_clientes_en_treeview = lambda tree: cargar_datos_en_treeview(tree, Cliente, COLUMNAS)

guardar_cliente = lambda data, tree, dialog, es_edicion: guardar_datos(
    Cliente, data, tree, dialog, claves_pk=['id_cliente'], es_edicion=es_edicion
)

eliminar_cliente_seleccionado = lambda tree: eliminar_seleccion(tree, Cliente, 'id_cliente')

obtener_datos_de_seleccion = obtener_datos_de_treeview
