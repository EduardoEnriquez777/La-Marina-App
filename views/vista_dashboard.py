import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import time
import os
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def cargar_fuente(archivo, size, bold=False):
    if os.path.exists(archivo):
        try:
            return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")
        except:
            return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")
    else:
        return font.Font(family="Genova", size=size, weight="bold" if bold else "normal")

def crear_dashboard(parent, navegadores_modulos):
    # === FUENTES ===
    fuente_titulo = cargar_fuente("genova.ttf", 40, True)
    fuente_botones = cargar_fuente("genova.ttf", 16, True)
    fuente_fecha = cargar_fuente("genova.ttf", 14)
    fuente_hora = cargar_fuente("genova.ttf", 24, True)

    # === COLORES E ICONOS POR DEFECTO ===
    MODULOS = {
        "Empleados": {"icono": "👤", "color": "#4ade80", "texto": "#111111"},
        "Proveedores": {"icono": "📦", "color": "#4ade80", "texto": "#111111"},
        "Cajas": {"icono": "💵", "color": "#4ade80", "texto": "#111111"},
        "Clientes": {"icono": "👥", "color": "#4ade80", "texto": "#111111"},
        "Sucursales": {"icono": "🏢", "color": "#4ade80", "texto": "#111111"},
        "Met. Pago": {"icono": "💳", "color": "#4ade80", "texto": "#111111"},
        "Almacenes": {"icono": "🏬", "color": "#4ade80", "texto": "#111111"},
    }

    frame = tk.Frame(parent, bg="white", width=1000, height=600)
    frame.pack_propagate(False)

    # === LOGO ===
    logo_path = os.path.join("icons", "logo.png")
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        # Cambio aquí: aumentar tamaño manteniendo proporción, ancho a 350, alto calculado proporcional
        max_width = 350
        max_height = 115
        logo_img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(frame, image=logo_tk, bg="white")
        logo_label.image = logo_tk
        logo_label.place(x=50, y=80)

    # === BOTONES DE MÓDULOS (dos columnas bien espaciadas) ===
    x_izq = 30
    y_inicio = 180
    espacio_y = 75
    ancho_boton = 240

    modulos_lista = list(navegadores_modulos.items())
    mitad = (len(modulos_lista) + 1) // 2
    for idx, (modulo, accion) in enumerate(modulos_lista):
        columna = 0 if idx < mitad else 1
        fila = idx if idx < mitad else idx - mitad

        x = x_izq + columna * (ancho_boton + 40)  # un poco más de separación horizontal
        y = y_inicio + fila * espacio_y

        datos = MODULOS.get(modulo, {"icono": "🔘", "color": "#4ade80", "texto": "#111111"})

        btn = tk.Button(
            frame,
            text=f"{datos['icono']}  {modulo}",
            font=fuente_botones,
            bg=datos["color"],
            fg=datos["texto"],
            activebackground="#16a34a",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=8,
            width=18,
            anchor="w",
            command=accion
        )
        btn.place(x=x, y=y)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#16a34a", fg="white"))
        btn.bind("<Leave>", lambda e, b=btn, c=datos["color"], f=datos["texto"]: b.config(bg=c, fg=f))

    # === IMAGEN LATERAL ===
    layer_path = os.path.join("icons", "layer.jpg")
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
    parent.resizable(False, False)

    return frame