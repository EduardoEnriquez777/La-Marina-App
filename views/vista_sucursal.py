import tkinter as tk
from tkinter import font, ttk, messagebox
from PIL import Image, ImageTk
import os
import time
import locale

from controllers.controlador_sucursal import (
    cargar_sucursals_en_treeview,
    guardar_sucursal,
    eliminar_sucursal_seleccionado
)

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def cargar_fuente(archivo, size, bold=False):
    if os.path.exists(archivo):
        try:
            return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")
        except Exception:
            return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")
    else:
        return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")

def crear_vista_sucursal(root, volver_callback):
    fuente_titulo   = cargar_fuente("genova.ttf", 28, True)
    fuente_label    = cargar_fuente("genova.ttf", 14)
    fuente_entrada  = cargar_fuente("genova.ttf", 13)
    fuente_boton    = cargar_fuente("genova.ttf", 13, True)
    fuente_fecha    = cargar_fuente("genova.ttf", 12)
    fuente_hora     = cargar_fuente("genova.ttf", 22, True)

    frame = tk.Frame(root, bg="white", width=1000, height=600)
    frame.pack_propagate(False)
    frame.pack()

    tk.Label(frame, text="\ud83c\udfec  Sucursales", font=fuente_titulo, bg="white", fg="#111111").place(x=30, y=20)

    columnas = ["id_sucursal", "nombre", "direccion", "ciudad", "estado", "codigo_postal", "telefono"]
    tree = ttk.Treeview(frame, columns=columnas, show="headings", selectmode="browse")
    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, anchor="center", width=110)
    tree.place(x=30, y=80, width=550, height=300)

    def abrir_dialogo(editar=False):
        dialog = tk.Toplevel(root)
        dialog.title("Editar Sucursal" if editar else "Agregar Sucursal")
        dialog.geometry("470x360")
        dialog.config(bg="white")

        campos = [
            {"etiqueta": "ID", "columna": "id_sucursal"},
            {"etiqueta": "Nombre", "columna": "nombre"},
            {"etiqueta": "Direcci\u00f3n", "columna": "direccion"},
            {"etiqueta": "Ciudad", "columna": "ciudad"},
            {"etiqueta": "Estado", "columna": "estado"},
            {"etiqueta": "C\u00f3digo Postal", "columna": "codigo_postal"},
            {"etiqueta": "Tel\u00e9fono", "columna": "telefono"}
        ]

        entradas = {}
        y_base = 20
        for i, campo in enumerate(campos):
            y = y_base + i * 40
            tk.Label(dialog, text=campo["etiqueta"], font=fuente_label, bg="white").place(x=20, y=y)
            entry = tk.Entry(dialog, font=fuente_entrada, relief="flat", bg="white")
            entry.place(x=180, y=y, width=250)
            entradas[campo["columna"]] = entry

        if editar:
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Aviso", "Seleccione una sucursal para editar")
                dialog.destroy()
                return
            datos = tree.item(seleccion[0])['values']
            for i, col in enumerate(columnas):
                entradas[col].insert(0, datos[i])
            entradas["id_sucursal"].config(state="readonly")

        def on_guardar():
            datos_nuevos = {clave: entrada.get().strip() for clave, entrada in entradas.items()}
            if not datos_nuevos["nombre"]:
                messagebox.showerror("Error", "El campo Nombre es obligatorio", parent=dialog)
                return
            try:
                guardar_sucursal(datos_nuevos, tree, dialog, editar)
                cargar_sucursals_en_treeview(tree)
                messagebox.showinfo("\u00c9xito", "Sucursal guardada correctamente", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=dialog)

        tk.Button(dialog, text="Guardar", font=fuente_boton, bg="#4ade80", fg="#111111",
                  activebackground="#16a34a", activeforeground="white",
                  relief="flat", padx=10, pady=5, width=12,
                  command=on_guardar).place(x=180, y=y_base + len(campos)*40 + 10)

    def on_eliminar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione una sucursal para eliminar")
            return
        confirmar = messagebox.askyesno("Confirmar", "\u00bfDesea eliminar la sucursal seleccionada?")
        if confirmar:
            try:
                eliminar_sucursal_seleccionado(tree)
                cargar_sucursals_en_treeview(tree)
                messagebox.showinfo("\u00c9xito", "Sucursal eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    botones = [
        ("Agregar", lambda: abrir_dialogo(editar=False)),
        ("Editar", lambda: abrir_dialogo(editar=True)),
        ("Eliminar", on_eliminar),
        ("Volver", volver_callback)
    ]
    btn_y = 400
    btn_x = 30
    espaciado = 140
    for i, (texto, accion) in enumerate(botones):
        btn = tk.Button(frame, text=texto, font=fuente_boton,
                        bg="#4ade80", fg="#111111",
                        activebackground="#16a34a", activeforeground="white",
                        relief="flat", padx=10, pady=5, width=9,
                        command=accion)
        btn.place(x=btn_x + i * espaciado, y=btn_y)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#16a34a", fg="white"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#4ade80", fg="#111111"))

    # Imagen lateral
    img_path = os.path.join("icons", "layer6.jpg")
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img.thumbnail((440, 480), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        label_img = tk.Label(frame, image=img_tk, bg="white")
        label_img.image = img_tk
        label_img.place(x=600, y=70)

    # Fecha y hora
    fecha_label = tk.Label(frame, font=fuente_fecha, fg="white", bg="#000000")
    fecha_label.place(x=680, y=80)
    hora_label = tk.Label(frame, font=fuente_hora, fg="white", bg="#000000")
    hora_label.place(x=743, y=110)

    def actualizar_fecha_hora():
        ahora = time.localtime()
        fecha_str = time.strftime("%A, %d de %B", ahora).capitalize()
        hora_str = time.strftime("%I:%M %p", ahora).lower()
        fecha_label.config(text=fecha_str)
        hora_label.config(text=hora_str)
        frame.after(1000, actualizar_fecha_hora)

    actualizar_fecha_hora()

    root.resizable(False, False)
    cargar_sucursals_en_treeview(tree)

    return frame
