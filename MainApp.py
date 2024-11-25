import tkinter as tk
from BaseDatos import BaseDatos
from InterfazInicio import InterfazInicio

def main():
    db = BaseDatos()
    ventana = tk.Tk()
    app = InterfazInicio(ventana, db)
    ventana.mainloop()
    db.cerrar_conexion()

if __name__ == "__main__":
    main()

