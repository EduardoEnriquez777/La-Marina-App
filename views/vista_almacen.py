import tkinter as tk
from tkinter import font, ttk, messagebox
from PIL import Image, ImageTk
import os
import time
import locale

from controllers.controlador_almacen import (
    cargar_almacens_en_treeview,
    guardar_almacen,
    eliminar_almacen_seleccionado,
    obtener_datos_de_seleccion
)

# Configurar locale en español para la fecha.
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def cargar_fuente(archivo, size, bold=False):
    if os.path.exists(archivo):
        try:
            return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")
        except Exception:
            return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")
    else:
        return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")

def crear_vista_almacen(root, volver_callback):
    # Definir las fuentes personalizadas.
    fuente_titulo   = cargar_fuente("genova.ttf", 28, True)
    fuente_label    = cargar_fuente("genova.ttf", 14)
    fuente_entrada  = cargar_fuente("genova.ttf", 13)
    fuente_boton    = cargar_fuente("genova.ttf", 13, True)
    fuente_fecha    = cargar_fuente("genova.ttf", 12)
    fuente_hora     = cargar_fuente("genova.ttf", 22, True)
    
    frame = tk.Frame(root, bg="white", width=1000, height=600)
    frame.pack_propagate(False)
    frame.pack()
    
    tk.Label(frame, text="🏬  Almacenes", font=fuente_titulo, bg="white", fg="#111111")\
        .place(x=30, y=20)
    
    # Ajuste del Treeview para que no estorbe la imagen lateral
    columnas = ["idalmacen", "nombre", "ubicacion", "capacidad_maxima", "estado"]
    tree = ttk.Treeview(frame, columns=columnas, show="headings", selectmode="browse")
    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center", width=100)  # ancho reducido para cada columna
    tree.place(x=30, y=80, width=550, height=300)  # menos ancho para dejar espacio a la imagen
    
    # Funciones abrir diálogo y eliminar (sin cambios)
    def abrir_dialogo_agregar():
        dialog = tk.Toplevel(root)
        dialog.title("Agregar Almacén")
        dialog.geometry("450x300")
        dialog.config(bg="white")
        
        campos_dialog = [
            {"etiqueta": "ID", "columna": "idalmacen"},
            {"etiqueta": "Nombre", "columna": "nombre"},
            {"etiqueta": "Ubicación", "columna": "ubicacion"},
            {"etiqueta": "Capacidad Máxima", "columna": "capacidad_maxima"},
            {"etiqueta": "Estado", "columna": "estado", "tipo": "combobox", "opciones": ["Activo", "Inactivo"]}
        ]
        
        entradas_dialog = {}
        y_base_dialog = 20
        for i, campo in enumerate(campos_dialog):
            y = y_base_dialog + i * 40
            tk.Label(dialog, text=campo["etiqueta"], font=fuente_label, bg="white", anchor="w")\
                .place(x=20, y=y)
            if campo.get("tipo") == "combobox":
                combo = ttk.Combobox(dialog, values=campo["opciones"], font=fuente_entrada, state="readonly")
                combo.place(x=180, y=y, width=220)
                entradas_dialog[campo["columna"]] = combo
            else:
                entry = tk.Entry(dialog, font=fuente_entrada, relief="flat", bg="white", fg="#111111")
                entry.place(x=180, y=y, width=220)
                entradas_dialog[campo["columna"]] = entry
        
        entradas_dialog["idalmacen"].config(state="normal")
        entradas_dialog["idalmacen"].delete(0, tk.END)
        entradas_dialog["idalmacen"].config(state="readonly")
        
        def on_guardar_dialogo():
            nuevos_datos = {
                "idalmacen": entradas_dialog["idalmacen"].get().strip(),
                "nombre": entradas_dialog["nombre"].get().strip(),
                "ubicacion": entradas_dialog["ubicacion"].get().strip(),
                "capacidad_maxima": entradas_dialog["capacidad_maxima"].get().strip(),
                "estado": entradas_dialog["estado"].get().strip()
            }
            if not nuevos_datos["nombre"]:
                messagebox.showerror("Error", "El campo Nombre es obligatorio", parent=dialog)
                return
            if nuevos_datos["capacidad_maxima"]:
                try:
                    nuevos_datos["capacidad_maxima"] = int(nuevos_datos["capacidad_maxima"])
                except ValueError:
                    messagebox.showerror("Error", "Capacidad Máxima debe ser un número entero", parent=dialog)
                    return
            else:
                nuevos_datos["capacidad_maxima"] = 0
            try:
                guardar_almacen(nuevos_datos, tree, dialog, False)
                cargar_almacens_en_treeview(tree)
                messagebox.showinfo("Éxito", "Almacén agregado correctamente", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=dialog)
        
        tk.Button(dialog, text="Guardar", font=fuente_boton, bg="#4ade80", fg="#111111",
                  activebackground="#16a34a", activeforeground="white",
                  relief="flat", padx=10, pady=5, width=12,
                  command=on_guardar_dialogo)\
            .place(x=180, y=y_base_dialog + len(campos_dialog)*40 + 10)
    
    def abrir_dialogo_editar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro para editar")
            return
        item = tree.item(seleccion[0])
        datos = item['values']
        
        dialog = tk.Toplevel(root)
        dialog.title("Editar Almacén")
        dialog.geometry("450x300")
        dialog.config(bg="white")
        
        campos_dialog = [
            {"etiqueta": "ID", "columna": "idalmacen"},
            {"etiqueta": "Nombre", "columna": "nombre"},
            {"etiqueta": "Ubicación", "columna": "ubicacion"},
            {"etiqueta": "Capacidad Máxima", "columna": "capacidad_maxima"},
            {"etiqueta": "Estado", "columna": "estado", "tipo": "combobox", "opciones": ["Activo", "Inactivo"]}
        ]
        
        entradas_dialog = {}
        y_base_dialog = 20
        for i, campo in enumerate(campos_dialog):
            y = y_base_dialog + i * 40
            tk.Label(dialog, text=campo["etiqueta"], font=fuente_label, bg="white", anchor="w")\
                .place(x=20, y=y)
            if campo.get("tipo") == "combobox":
                combo = ttk.Combobox(dialog, values=campo["opciones"], font=fuente_entrada, state="readonly")
                combo.place(x=180, y=y, width=220)
                entradas_dialog[campo["columna"]] = combo
            else:
                entry = tk.Entry(dialog, font=fuente_entrada, relief="flat", bg="white", fg="#111111")
                entry.place(x=180, y=y, width=220)
                entradas_dialog[campo["columna"]] = entry
        
        entradas_dialog["idalmacen"].config(state="normal")
        entradas_dialog["idalmacen"].delete(0, tk.END)
        entradas_dialog["idalmacen"].insert(0, datos[0])
        entradas_dialog["idalmacen"].config(state="readonly")
        for i, col in enumerate(["nombre", "ubicacion", "capacidad_maxima", "estado"]):
            widget = entradas_dialog[col]
            widget.delete(0, tk.END)
            widget.insert(0, datos[i+1])
        
        def on_guardar_dialogo():
            nuevos_datos = {
                "idalmacen": entradas_dialog["idalmacen"].get().strip(),
                "nombre": entradas_dialog["nombre"].get().strip(),
                "ubicacion": entradas_dialog["ubicacion"].get().strip(),
                "capacidad_maxima": entradas_dialog["capacidad_maxima"].get().strip(),
                "estado": entradas_dialog["estado"].get().strip()
            }
            if not nuevos_datos["nombre"]:
                messagebox.showerror("Error", "El campo Nombre es obligatorio", parent=dialog)
                return
            if nuevos_datos["capacidad_maxima"]:
                try:
                    nuevos_datos["capacidad_maxima"] = int(nuevos_datos["capacidad_maxima"])
                except ValueError:
                    messagebox.showerror("Error", "Capacidad Máxima debe ser un número entero", parent=dialog)
                    return
            else:
                nuevos_datos["capacidad_maxima"] = 0
            try:
                guardar_almacen(nuevos_datos, tree, dialog, True)
                cargar_almacens_en_treeview(tree)
                messagebox.showinfo("Éxito", "Almacén actualizado correctamente", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=dialog)
        
        tk.Button(dialog, text="Guardar", font=fuente_boton, bg="#4ade80", fg="#111111",
                  activebackground="#16a34a", activeforeground="white",
                  relief="flat", padx=10, pady=5, width=12,
                  command=on_guardar_dialogo)\
            .place(x=180, y=y_base_dialog + len(campos_dialog)*40 + 10)
    
    def on_eliminar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro para eliminar")
            return
        id_seleccionado = tree.item(seleccion[0])['values'][0]
        if not id_seleccionado:
            messagebox.showerror("Error", "No hay ID seleccionado para eliminar")
            return
        
        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este almacén?")
        if confirmar:
            try:
                eliminar_almacen_seleccionado(tree)
                cargar_almacens_en_treeview(tree)
                messagebox.showinfo("Éxito", "Almacén eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")
    
    # Botones alineados horizontalmente debajo de la tabla
    botones = [
        ("Agregar", abrir_dialogo_agregar),
        ("Editar", abrir_dialogo_editar),
        ("Eliminar", on_eliminar),
        ("Volver", volver_callback)
    ]
    btn_y = 400
    btn_x_inicio = 30
    btn_espacio = 140  # separación horizontal entre botones
    
    for idx, (texto, accion) in enumerate(botones):
        btn = tk.Button(
            frame, text=texto, font=fuente_boton,
            bg="#4ade80", fg="#111111",
            activebackground="#16a34a", activeforeground="white",
            relief="flat", padx=10, pady=5, width=9,
            command=accion
        )
        btn.place(x=btn_x_inicio + idx * btn_espacio, y=btn_y)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#16a34a", fg="white"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#4ade80", fg="#111111"))
    
    # === IMAGEN LATERAL ===
    layer_path = os.path.join("icons", "layer2.jpg")
    if os.path.exists(layer_path):
        layer_img = Image.open(layer_path)
        layer_img.thumbnail((440, 480), Image.Resampling.LANCZOS)
        layer_tk = ImageTk.PhotoImage(layer_img)
        layer_label = tk.Label(frame, image=layer_tk, bg="white")
        layer_label.image = layer_tk
        layer_label.place(x=600, y=70)

    # === FECHA Y HORA ===
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

    # === DESACTIVAR MAXIMIZAR VENTANA ===
    root.resizable(False, False)

    # Cargar datos en la tabla inicialmente
    cargar_almacens_en_treeview(tree)

    return frame