import tkinter as tk
from tkinter import font, ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
import time
import locale
from datetime import datetime  # 🔒 Validación de fecha

from controllers.controlador_caja import (
    cargar_cajas_en_treeview,
    guardar_caja,
    eliminar_caja_seleccionado,
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

def crear_vista_caja(root, volver_callback):
    fuente_titulo = cargar_fuente("genova.ttf", 28, True)
    fuente_label = cargar_fuente("genova.ttf", 14)
    fuente_entrada = cargar_fuente("genova.ttf", 13)
    fuente_boton = cargar_fuente("genova.ttf", 13, True)
    fuente_fecha = cargar_fuente("genova.ttf", 12)
    fuente_hora = cargar_fuente("genova.ttf", 22, True)

    frame = tk.Frame(root, bg="white", width=1000, height=600)
    frame.pack_propagate(False)
    frame.pack()

    tk.Label(frame, text="💵  Cajas", font=fuente_titulo, bg="white", fg="#111111").place(x=30, y=20)

    columnas = ["idcaja", "saldo_inicial", "fecha_apertura", "saldo_final", "fecha_cierre"]
    tree = ttk.Treeview(frame, columns=columnas, show="headings", selectmode="browse")
    for col in columnas:
        tree.heading(col, text=col.capitalize().replace("_", " "))
        tree.column(col, anchor="center", width=100)
    tree.place(x=30, y=80, width=550, height=300)

    def abrir_dialogo_caja(editar=False):
        seleccion = tree.selection()
        datos = {}
        if editar:
            if not seleccion:
                messagebox.showwarning("Aviso", "Seleccione un registro para editar")
                return
            item = tree.item(seleccion[0])
            valores = item['values']
            datos = dict(zip(columnas, valores))

        dialog = tk.Toplevel(root)
        dialog.title("Editar Caja" if editar else "Agregar Caja")
        dialog.geometry("480x380")
        dialog.config(bg="white")

        campos_dialog = [
            {"etiqueta": "ID", "columna": "idcaja"},
            {"etiqueta": "Saldo Inicial", "columna": "saldo_inicial"},
            {"etiqueta": "Fecha Apertura", "columna": "fecha_apertura", "tipo": "fecha_hora"},
            {"etiqueta": "Saldo Final", "columna": "saldo_final"},
            {"etiqueta": "Fecha Cierre", "columna": "fecha_cierre", "tipo": "fecha_hora"}
        ]

        entradas = {}

        for i, campo in enumerate(campos_dialog):
            y = 20 + i * 60
            tk.Label(dialog, text=campo["etiqueta"], font=fuente_label, bg="white").place(x=20, y=y)

            if campo.get("tipo") == "fecha_hora":
                fecha = DateEntry(dialog, font=fuente_entrada, date_pattern="yyyy-mm-dd", width=12)
                fecha.place(x=180, y=y)

                hora = ttk.Combobox(dialog, values=[f"{h:02}" for h in range(0, 24)], width=3, font=fuente_entrada)
                hora.place(x=310, y=y)
                minuto = ttk.Combobox(dialog, values=[f"{m:02}" for m in range(0, 60, 5)], width=3, font=fuente_entrada)
                minuto.place(x=360, y=y)

                entradas[campo["columna"]] = {"fecha": fecha, "hora": hora, "minuto": minuto}
            else:
                entry = tk.Entry(dialog, font=fuente_entrada, relief="flat", bg="white", fg="#111111", width=22)
                entry.place(x=180, y=y)
                entradas[campo["columna"]] = entry

        if editar:
            for campo in campos_dialog:
                clave = campo["columna"]
                valor = datos.get(clave, "")
                if campo.get("tipo") == "fecha_hora" and valor:
                    fecha_str, hora_str = valor.split(" ")
                    fecha_val = fecha_str.strip()
                    hora_val, minuto_val, *_ = hora_str.split(":")
                    entradas[clave]["fecha"].set_date(fecha_val)
                    entradas[clave]["hora"].set(hora_val)
                    entradas[clave]["minuto"].set(minuto_val)
                else:
                    entradas[clave].insert(0, valor)
            entradas["idcaja"].config(state="readonly")
        else:
            entradas["idcaja"].config(state="normal")

        def on_guardar():
            nuevos_datos = {}
            for campo in campos_dialog:
                clave = campo["columna"]
                if campo.get("tipo") == "fecha_hora":
                    fecha = entradas[clave]["fecha"].get()
                    hora = entradas[clave]["hora"].get()
                    minuto = entradas[clave]["minuto"].get()
                    if not hora or not minuto:
                        messagebox.showerror("Error", f"Debe completar la hora de {clave}", parent=dialog)
                        return
                    nuevos_datos[clave] = f"{fecha} {hora}:{minuto}:00"
                else:
                    valor = entradas[clave].get().strip()
                    nuevos_datos[clave] = valor

            # 🔒 Validación de fecha: evitar fechas futuras
            for clave in ["fecha_apertura", "fecha_cierre"]:
                valor = nuevos_datos.get(clave, "")
                if valor:
                    try:
                        fecha_formato = "%Y-%m-%d %H:%M:%S"
                        fecha_dt = datetime.strptime(valor, fecha_formato)
                        if fecha_dt > datetime.now():
                            messagebox.showerror("Error", f"La {clave.replace('_', ' ')} no puede ser mayor que la fecha actual.", parent=dialog)
                            return
                    except ValueError:
                        messagebox.showerror("Error", f"Formato inválido en {clave.replace('_', ' ')}", parent=dialog)
                        return

            if not nuevos_datos["saldo_inicial"]:
                messagebox.showerror("Error", "El campo Saldo Inicial es obligatorio", parent=dialog)
                return

            try:
                guardar_caja(nuevos_datos, tree, dialog, editar)
                cargar_cajas_en_treeview(tree)
                messagebox.showinfo("Éxito", "Caja guardada correctamente", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=dialog)

        tk.Button(dialog, text="Guardar", font=fuente_boton, bg="#4ade80", fg="#111111",
                  activebackground="#16a34a", activeforeground="white",
                  relief="flat", padx=10, pady=5, width=12, command=on_guardar)\
            .place(x=180, y=320)

    def eliminar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro para eliminar")
            return
        confirmar = messagebox.askyesno("Confirmar", "¿Desea eliminar esta caja?")
        if confirmar:
            try:
                eliminar_caja_seleccionado(tree)
                cargar_cajas_en_treeview(tree)
                messagebox.showinfo("Éxito", "Caja eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    botones = [
        ("Agregar", lambda: abrir_dialogo_caja(False)),
        ("Editar", lambda: abrir_dialogo_caja(True)),
        ("Eliminar", eliminar),
        ("Volver", volver_callback)
    ]

    btn_y = 400
    btn_x_inicio = 30
    btn_espacio = 140
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

    layer_path = os.path.join("icons", "layer4.jpg")
    if os.path.exists(layer_path):
        layer_img = Image.open(layer_path)
        layer_img.thumbnail((440, 480), Image.Resampling.LANCZOS)
        layer_tk = ImageTk.PhotoImage(layer_img)
        layer_label = tk.Label(frame, image=layer_tk, bg="white")
        layer_label.image = layer_tk
        layer_label.place(x=600, y=70)

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
    cargar_cajas_en_treeview(tree)

    return frame
