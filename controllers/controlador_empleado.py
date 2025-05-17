from controllers.controlador_generico import *
from model.modelo_empleado import Empleado
from model import SessionLocal
from model import Sucursal

COLUMNAS = ['id_empleado', 'nombre', 'apellido', 'cargo', 'fecha_contratacion', 'salario', 'id_sucursal']

cargar_empleado_en_treeview = lambda tree: cargar_datos_en_treeview(tree, Empleado, COLUMNAS)

guardar_empleado = lambda data, tree, dialog, es_edicion: guardar_datos(
    Empleado, data, tree, dialog, claves_pk=['id_empleado'], es_edicion=es_edicion
)

eliminar_empleado_seleccionado = lambda tree: eliminar_seleccion(tree, Empleado, 'id_empleado')

obtener_datos_de_seleccion = obtener_datos_de_treeview

def obtener_ids_sucursal():
    try:
        db = SessionLocal()
        return [str(s.id_sucursal) for s in db.query(Sucursal).all()]
    finally:
        db.close()