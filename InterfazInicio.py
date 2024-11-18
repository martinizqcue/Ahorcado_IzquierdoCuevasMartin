import tkinter as tk
from tkinter import messagebox

from InterfazJuego import InterfazJuego

class InterfazInicio:
    def __init__(self, ventana, db):
        self.ventana = ventana
        self.db = db
        self.jugador_var = None  # Inicializa la variable para el nombre del jugador
        self.crear_interfaz()

    def crear_interfaz(self):
        label_bienvenida = tk.Label(self.ventana, text="Bienvenido al Juego del Ahorcado")
        label_bienvenida.pack()

        self.jugador_seleccionado = None
        self.tematica_seleccionada = None

        # Dropdown para seleccionar jugador
        self.seleccionar_jugador()

        # Dropdown para seleccionar temática
        self.seleccionar_tematica()

        # Botón para iniciar el juego
        btn_iniciar = tk.Button(self.ventana, text="Iniciar Juego", command=self.iniciar_juego)
        btn_iniciar.pack()

    def seleccionar_jugador(self):
        label_jugador = tk.Label(self.ventana, text="Ingresa tu nombre:")
        label_jugador.pack(pady=10)

        self.jugador_var = tk.StringVar(self.ventana)  # Variable para almacenar el nombre del jugador
        entry_jugador = tk.Entry(self.ventana, textvariable=self.jugador_var)
        entry_jugador.pack(pady=5)

        btn_registrar = tk.Button(self.ventana, text="Registrar", command=self.registrar_jugador)
        btn_registrar.pack(pady=10)

    def registrar_jugador(self):
        nombre_jugador = self.jugador_var.get().strip()
        if nombre_jugador:
            self.db.registrar_jugador(nombre_jugador)  # Registra al jugador en la base de datos
            messagebox.showinfo("Registro", f"Jugador registrado: {nombre_jugador}")
            self.jugador_var.set("")  # Limpia el campo de entrada
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre.")

    def seleccionar_tematica(self):
        label_tematica = tk.Label(self.ventana, text="Selecciona una temática:")
        label_tematica.pack()

        tematicas = self.db.obtener_tematica()
        self.tematica_var = tk.StringVar(self.ventana)
        self.tematica_var.set(tematicas[0][1] if tematicas else "Ninguna")  # Valor por defecto

        dropdown_tematica = tk.OptionMenu(self.ventana, self.tematica_var, *[f"{tematica[1]}" for tematica in tematicas])
        dropdown_tematica.pack()

    def iniciar_juego(self):
        # Obtener el ID del jugador seleccionado
        jugadores = self.db.obtener_jugadores()
        jugador_id = next((jugador[0] for jugador in jugadores if jugador[1] == self.jugador_var.get()), None)

        # Obtener el ID de la temática seleccionada
        tematicas = self.db.obtener_tematica()
        tematica_id = next((tematica[0] for tematica in tematicas if tematica[1] == self.tematica_var.get()), None)

        if jugador_id and tematica_id:
            jugador = (jugador_id, self.jugador_var.get())
            tematica_data = {"id": tematica_id, "nombre": self.tematica_var.get()}
            ventana_juego = tk.Toplevel(self.ventana)  # Crear una nueva ventana para el juego
            InterfazJuego(ventana_juego, self.db, jugador, tematica_data)  # Iniciar la interfaz del juego
        else:
            print("Por favor, selecciona un jugador y una temática.")



