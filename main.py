import tkinter as tk
from views.vista_dashboard import crear_dashboard
from views.vista_proveedor import crear_vista_proveedor
from views.vista_sucursal import crear_vista_sucursal
from views.vista_almacen import crear_vista_almacen
from views.vista_caja import crear_vista_caja
from views.vista_cliente import crear_vista_cliente
from views.vista_empleado import crear_vista_empleado
from views.vista_metodo_pago import crear_vista_metodo_pago

def main():
    root = tk.Tk()
    root.title("La Marina App")
    root.geometry("900x600")

    frame_actual = {"frame": None}

    def mostrar_frame(nuevo_frame_func):
        if frame_actual["frame"]:
            frame_actual["frame"].destroy()
        nuevo_frame = nuevo_frame_func()
        nuevo_frame.pack(fill="both", expand=True)  # Aquí se muestra el frame
        frame_actual["frame"] = nuevo_frame

    def volver_dashboard():
        mostrar_frame(lambda: crear_dashboard(root, navegadores_modulos))

    navegadores_modulos = {
        "Sucursales": lambda: mostrar_frame(lambda: crear_vista_sucursal(root, volver_dashboard)),
        "Empleados": lambda: mostrar_frame(lambda: crear_vista_empleado(root, volver_dashboard)),
        "Proveedores": lambda: mostrar_frame(lambda: crear_vista_proveedor(root, volver_dashboard)),
        "Almacenes": lambda: mostrar_frame(lambda: crear_vista_almacen(root, volver_dashboard)),
        "Clientes": lambda: mostrar_frame(lambda: crear_vista_cliente(root, volver_dashboard)),
        "Cajas": lambda: mostrar_frame(lambda: crear_vista_caja(root, volver_dashboard)),
        "Métodos de Pago": lambda: mostrar_frame(lambda: crear_vista_metodo_pago(root, volver_dashboard)),
    }

    mostrar_frame(lambda: crear_dashboard(root, navegadores_modulos))

    root.mainloop()

if __name__ == "__main__":
    main()
