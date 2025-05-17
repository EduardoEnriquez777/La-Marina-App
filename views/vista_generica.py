import tkinter as tk
from tkinter import ttk


def crear_vista_generica(root, nombre_entidad, campos, controlador, volver_callback):
    frame = ttk.Frame(root)

    # Botones superiores
    top_frame = ttk.Frame(frame)
    top_frame.pack(fill=tk.X, pady=5)

    ttk.Button(top_frame, text="Volver", command=volver_callback).pack(side=tk.LEFT, padx=5)
    ttk.Button(top_frame, text=f"Agregar {nombre_entidad}", command=lambda: abrir_dialogo(frame, campos, controlador)).pack(side=tk.LEFT, padx=5)

    # Tabla
    columnas = [campo["columna"] for campo in campos]
    tree = ttk.Treeview(frame, columns=columnas, show='headings')
    tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    for campo in campos:
        tree.heading(campo["columna"], text=campo["etiqueta"], anchor=tk.CENTER)
        tree.column(campo["columna"], width=140, anchor=tk.CENTER)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree.bind('<Double-1>', lambda event: editar_registro(tree, frame, campos, controlador))

    # Botones inferiores
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill=tk.X, pady=5)

    ttk.Button(btn_frame, text="Editar", command=lambda: editar_registro(tree, frame, campos, controlador)).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Eliminar", command=lambda: controlador["eliminar"](tree)).pack(side=tk.LEFT, padx=5)

    # Cargar datos
    controlador["cargar"](tree)

    frame.pack(fill=tk.BOTH, expand=True)
    return frame

def abrir_dialogo(parent, campos, controlador, datos=None):
    dialog = tk.Toplevel(parent)
    dialog.title("Editar" if datos else "Agregar")
    dialog.grab_set()

    entries = {}
    for i, campo in enumerate(campos):
        ttk.Label(dialog, text=campo["etiqueta"] + ":").grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)

        tipo = campo.get("tipo", "entry")
        if tipo == "combobox":
            entry = ttk.Combobox(dialog, values=campo.get("opciones", []), state="readonly", width=28)
        else:
            entry = ttk.Entry(dialog, width=30)

        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[campo["columna"]] = entry

        if datos:
            entry.insert(0, datos[i])
            if campo.get("clave", False):
                entry.config(state='readonly')


    btn_frame = ttk.Frame(dialog)
    btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=10)

    ttk.Button(btn_frame, text="Guardar", command=lambda: controlador["guardar"](
        {k: e.get().strip() for k, e in entries.items()},
        parent.children['!treeview'],
        dialog,
        es_edicion=datos is not None
    )).pack(side=tk.LEFT, padx=5)

    ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

def editar_registro(tree, parent, campos, controlador):
    datos = controlador["obtener"](tree)
    if datos:
        abrir_dialogo(parent, campos, controlador, datos)

