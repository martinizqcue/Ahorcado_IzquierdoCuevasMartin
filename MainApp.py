from BaseDatos import BaseDatos
from InterfazJuego import InterfazJuego
from JuegoAhorcado import JuegoAhorcado

if __name__ == "__main__":
    from tkinter import Tk

    db = BaseDatos()
    juego = JuegoAhorcado(db)

    root = Tk()
    interfaz = InterfazJuego(root, db, juego)
    root.mainloop()
