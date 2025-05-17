import tkinter as tk
from tkinter import font, ttk, messagebox
from PIL import Image, ImageTk
import os
import time
import locale

from controllers.controlador_cliente import (
    cargar_clientes_en_treeview,
    guardar_cliente,
    eliminar_cliente_seleccionado,
    obtener_datos_de_seleccion
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

def crear_vista_cliente(root, volver_callback):
    fuente_titulo   = cargar_fuente("genova.ttf", 28, True)
    fuente_label    = cargar_fuente("genova.ttf", 14)
    fuente_entrada  = cargar_fuente("genova.ttf", 13)
    fuente_boton    = cargar_fuente("genova.ttf", 13, True)
    fuente_fecha    = cargar_fuente("genova.ttf", 12)
    fuente_hora     = cargar_fuente("genova.ttf", 22, True)

    frame = tk.Frame(root, bg="white", width=1000, height=600)
    frame.pack_propagate(False)
    frame.pack()

    tk.Label(frame, text="👤  Clientes", font=fuente_titulo, bg="white", fg="#111111")\
        .place(x=30, y=20)

    columnas = ["id_cliente", "nombre", "apellido", "telefono", "correo", "direccion"]
    tree = ttk.Treeview(frame, columns=columnas, show="headings", selectmode="browse")
    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center", width=100)
    tree.place(x=30, y=80, width=550, height=300)

    def abrir_dialogo_cliente(es_edicion=False):
        dialog = tk.Toplevel(root)
        dialog.title("Editar Cliente" if es_edicion else "Agregar Cliente")
        dialog.geometry("450x350")
        dialog.config(bg="white")

        campos = [
            {"etiqueta": "ID", "columna": "id_cliente"},
            {"etiqueta": "Nombre", "columna": "nombre"},
            {"etiqueta": "Apellido", "columna": "apellido"},
            {"etiqueta": "Teléfono", "columna": "telefono"},
            {"etiqueta": "Email", "columna": "correo"},
            {"etiqueta": "Dirección", "columna": "direccion"},
        ]

        entradas = {}
        y_base = 20
        for i, campo in enumerate(campos):
            y = y_base + i * 40
            tk.Label(dialog, text=campo["etiqueta"], font=fuente_label, bg="white").place(x=20, y=y)
            entry = tk.Entry(dialog, font=fuente_entrada, relief="flat", bg="white", fg="#111111")
            entry.place(x=180, y=y, width=220)
            entradas[campo["columna"]] = entry

        if es_edicion:
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Aviso", "Seleccione un cliente para editar")
                dialog.destroy()
                return
            datos = tree.item(seleccion[0])['values']
            for i, campo in enumerate(columnas):
                entradas[campo].insert(0, datos[i])
            entradas["id_cliente"].config(state="readonly")

        def on_guardar():
            datos_nuevos = {col: entradas[col].get().strip() for col in columnas}
            if not datos_nuevos["nombre"] or not datos_nuevos["apellido"]:
                messagebox.showerror("Error", "Los campos Nombre y Apellido son obligatorios", parent=dialog)
                return
            try:
                guardar_cliente(datos_nuevos, tree, dialog, es_edicion)
                cargar_clientes_en_treeview(tree)
                messagebox.showinfo("Éxito", "Cliente guardado correctamente", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=dialog)

        tk.Button(dialog, text="Guardar", font=fuente_boton, bg="#4ade80", fg="#111111",
                  activebackground="#16a34a", activeforeground="white",
                  relief="flat", padx=10, pady=5, width=12,
                  command=on_guardar).place(x=180, y=y_base + len(campos)*40 + 10)

    def on_eliminar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un cliente para eliminar")
            return
        id_sel = tree.item(seleccion[0])['values'][0]
        confirmar = messagebox.askyesno("Confirmar", f"¿Desea eliminar el cliente ID {id_sel}?")
        if confirmar:
            try:
                eliminar_cliente_seleccionado(tree)
                cargar_clientes_en_treeview(tree)
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    botones = [
        ("Agregar", lambda: abrir_dialogo_cliente(False)),
        ("Editar", lambda: abrir_dialogo_cliente(True)),
        ("Eliminar", on_eliminar),
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

    # Imagen decorativa lateral
    img_path = os.path.join("icons", "layer3.jpg"
    "")
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img.thumbnail((440, 480), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        label_img = tk.Label(frame, image=tk_img, bg="white")
        label_img.image = tk_img
        label_img.place(x=600, y=70)

    fecha_label = tk.Label(frame, font=fuente_fecha, fg="white", bg="#000000")
    fecha_label.place(x=680, y=80)
    hora_label = tk.Label(frame, font=fuente_hora, fg="white", bg="#000000")
    hora_label.place(x=743, y=110)

    def actualizar_fecha_hora():
        ahora = time.localtime()
        fecha = time.strftime("%A, %d de %B", ahora).capitalize()
        hora = time.strftime("%I:%M %p", ahora).lower()
        fecha_label.config(text=fecha)
        hora_label.config(text=hora)
        frame.after(1000, actualizar_fecha_hora)

    actualizar_fecha_hora()
    root.resizable(False, False)

    cargar_clientes_en_treeview(tree)
    return frame
