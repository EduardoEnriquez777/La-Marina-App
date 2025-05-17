from tkinter import messagebox
from sqlalchemy.exc import SQLAlchemyError
from model import SessionLocal

def cargar_datos_en_treeview(tree, modelo, columnas):
    tree.delete(*tree.get_children())
    try:
        db = SessionLocal()
        registros = db.query(modelo).all()
        for r in registros:
            valores = []
            for col in columnas:
                val = getattr(r, col)
                # Si el atributo tiene un .value (como los Enum), lo usamos
                if hasattr(val, 'value'):
                    val = val.value
                valores.append(val)
            tree.insert('', 'end', values=valores)
    except SQLAlchemyError as e:
        messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}")
    finally:
        db.close()


def guardar_datos(modelo, data, tree, dialog, claves_pk, es_edicion):
    try:
        db = SessionLocal()
        if es_edicion:
            filtro = {clave: data[clave] for clave in claves_pk}
            obj = db.query(modelo).filter_by(**filtro).first()
            if obj:
                for key, value in data.items():
                    if key not in claves_pk:
                        setattr(obj, key, value)
                db.commit()
                messagebox.showinfo("Éxito", "Registro actualizado")
            else:
                messagebox.showerror("Error", "Registro no encontrado")
        else:
            nuevo = modelo(**{k: v for k, v in data.items() if k not in claves_pk})
            db.add(nuevo)
            db.commit()
            messagebox.showinfo("Éxito", "Registro agregado")
        cargar_datos_en_treeview(tree, modelo, data.keys())
        dialog.destroy()
    except SQLAlchemyError as e:
        messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
    finally:
        db.close()

def eliminar_seleccion(tree, modelo, columna_id):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un registro")
        return

    if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
        return

    item_id = tree.item(seleccion[0])['values'][0]
    try:
        db = SessionLocal()
        obj = db.query(modelo).filter_by(**{columna_id: item_id}).first()
        if obj:
            db.delete(obj)
            db.commit()
            messagebox.showinfo("Éxito", "Registro eliminado")
            tree.delete(seleccion[0])
        else:
            messagebox.showerror("Error", "Registro no encontrado")
    except SQLAlchemyError as e:
        messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
    finally:
        db.close()

def obtener_datos_de_treeview(tree):
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un registro")
        return None
    return tree.item(seleccion[0])['values']
