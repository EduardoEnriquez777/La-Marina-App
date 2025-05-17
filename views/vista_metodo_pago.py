import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import os
import time
import locale

from controllers.controlador_metodo_pago import (
    cargar_metodo_pago_en_treeview,
    guardar_metodo_pago,
    eliminar_metodo_pago_seleccionado,
    obtener_datos_de_seleccion
)

# Configurar idioma local
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def cargar_fuente(archivo, size, bold=False):
    if os.path.exists(archivo):
        try:
            return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")
        except Exception:
            pass
    return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")

def crear_vista_metodo_pago(root, volver_callback):
    fuente_titulo   = cargar_fuente("genova.ttf", 28, True)
    fuente_label    = cargar_fuente("genova.ttf", 14)
    fuente_entrada  = cargar_fuente("genova.ttf", 13)
    fuente_boton    = cargar_fuente("genova.ttf", 13, True)
    fuente_fecha    = cargar_fuente("genova.ttf", 12)
    fuente_hora     = cargar_fuente("genova.ttf", 22, True)

    frame = tk.Frame(root, bg="white", width=1000, height=600)
    frame.pack_propagate(False)
    frame.pack()

    tk.Label(frame, text="💳  Métodos de Pago", font=fuente_titulo, bg="white", fg="#111111")\
        .place(x=30, y=20)

    columnas = ["idmetodo_pago", "nombre", "descripcion", "activo"]
    tree = ttk.Treeview(frame, columns=columnas, show="headings", selectmode="browse")
    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center", width=120)
    tree.place(x=30, y=80, width=550, height=300)

    def abrir_dialogo(editar=False):
        dialog = tk.Toplevel(root)
        dialog.title("Editar Método de Pago" if editar else "Agregar Método de Pago")
        dialog.geometry("450x250")
        dialog.config(bg="white")

        campos = [
            {"etiqueta": "ID", "columna": "idmetodo_pago"},
            {"etiqueta": "Nombre", "columna": "nombre"},
            {"etiqueta": "Descripción", "columna": "descripcion"},
            {"etiqueta": "Activo", "columna": "activo", "tipo": "combobox", "opciones": ["Si", "No"]}
        ]

        entradas = {}
        y_base = 20
        for i, campo in enumerate(campos):
            y = y_base + i * 40
            tk.Label(dialog, text=campo["etiqueta"], font=fuente_label, bg="white")\
                .place(x=20, y=y)
            if campo.get("tipo") == "combobox":
                combo = ttk.Combobox(dialog, values=campo["opciones"], font=fuente_entrada, state="readonly")
                combo.place(x=180, y=y, width=220)
                entradas[campo["columna"]] = combo
            else:
                entry = tk.Entry(dialog, font=fuente_entrada, relief="flat", bg="white")
                entry.place(x=180, y=y, width=220)
                entradas[campo["columna"]] = entry

        if editar:
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Aviso", "Seleccione un registro para editar")
                dialog.destroy()
                return
            datos = tree.item(seleccion[0])['values']
            for i, campo in enumerate(columnas):
                entradas[campo].insert(0, datos[i])
            entradas["idmetodo_pago"].config(state="readonly")
        else:
            entradas["idmetodo_pago"].config(state="normal")
            entradas["idmetodo_pago"].delete(0, tk.END)

        def guardar():
            data = {col: entradas[col].get().strip() for col in columnas}
            if not data["nombre"]:
                messagebox.showerror("Error", "El campo Nombre es obligatorio", parent=dialog)
                return
            try:
                guardar_metodo_pago(data, tree, dialog, editar)
                cargar_metodo_pago_en_treeview(tree)
                messagebox.showinfo("Éxito", "Guardado correctamente", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=dialog)

        tk.Button(dialog, text="Guardar", font=fuente_boton, bg="#4ade80", fg="#111111",
                  activebackground="#16a34a", activeforeground="white",
                  relief="flat", padx=10, pady=5, width=12, command=guardar)\
            .place(x=180, y=y_base + len(campos)*40 + 10)

    def eliminar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro para eliminar")
            return
        confirmar = messagebox.askyesno("Confirmar", "¿Desea eliminar el método de pago seleccionado?")
        if confirmar:
            try:
                eliminar_metodo_pago_seleccionado(tree)
                cargar_metodo_pago_en_treeview(tree)
                messagebox.showinfo("Éxito", "Eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    botones = [
        ("Agregar", lambda: abrir_dialogo(False)),
        ("Editar", lambda: abrir_dialogo(True)),
        ("Eliminar", eliminar),
        ("Volver", volver_callback)
    ]
    btn_y = 400
    btn_x_inicio = 30
    btn_espacio = 140

    for idx, (texto, accion) in enumerate(botones):
        btn = tk.Button(frame, text=texto, font=fuente_boton,
                        bg="#4ade80", fg="#111111",
                        activebackground="#16a34a", activeforeground="white",
                        relief="flat", padx=10, pady=5, width=9,
                        command=accion)
        btn.place(x=btn_x_inicio + idx * btn_espacio, y=btn_y)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#16a34a", fg="white"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#4ade80", fg="#111111"))

    # Imagen lateral
    layer_path = os.path.join("icons", "layer8.jpg")
    if os.path.exists(layer_path):
        img = Image.open(layer_path)
        img.thumbnail((440, 480), Image.Resampling.LANCZOS)
        layer_tk = ImageTk.PhotoImage(img)
        label_img = tk.Label(frame, image=layer_tk, bg="white")
        label_img.image = layer_tk
        label_img.place(x=600, y=70)

    # Fecha y hora
    fecha_label = tk.Label(frame, font=fuente_fecha, fg="white", bg="#000000")
    fecha_label.place(x=680, y=80)
    hora_label = tk.Label(frame, font=fuente_hora, fg="white", bg="#000000")
    hora_label.place(x=743, y=110)

    def actualizar_fecha_hora():
        ahora = time.localtime()
        fecha_label.config(text=time.strftime("%A, %d de %B", ahora).capitalize())
        hora_label.config(text=time.strftime("%I:%M %p", ahora).lower())
        frame.after(1000, actualizar_fecha_hora)

    actualizar_fecha_hora()

    root.resizable(False, False)
    cargar_metodo_pago_en_treeview(tree)
    return frame
