import tkinter as tk
from tkinter import messagebox
import mysql
from InterfazJuego import InterfazJuego

class InterfazInicio:
    def __init__(self, ventana, db):
        self.ventana = ventana
        self.db = db
        self.jugador_var = None  # Inicializa la variable para el nombre del jugador
        self.crear_interfaz()

    def crear_interfaz(self):
        self.ventana.title("Juego del Ahorcado")

        self.ventana.resizable(False, False)
        self.ventana.configure(bg="spring green")

        self.centrar_ventana()

        label_bienvenida = tk.Label(self.ventana, text="Bienvenido al Juego del Ahorcado", bg="spring green", font=("Arial", 16, 'bold'))
        label_bienvenida.pack(pady=20)

        self.jugador_seleccionado = None
        self.tematica_seleccionada = None

        # Dropdown para seleccionar jugador
        self.seleccionar_jugador()

        # Dropdown para seleccionar temática
        self.seleccionar_tematica()

        # Botón para iniciar el juego
        btn_iniciar = tk.Button(self.ventana, text="Iniciar Juego", command=self.iniciar_juego, bg="gold", font=("Arial", 12, 'bold'))
        btn_iniciar.pack(pady=20)

    def centrar_ventana(self):
        # Obtener el tamaño de la pantalla
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()

        # Obtener el tamaño de la ventana
        ancho_ventana = 400
        alto_ventana = 400

        # Calcular la posición x, y para centrar la ventana
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        # Colocar la ventana en la posición calculada
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    def seleccionar_jugador(self):
        label_jugador = tk.Label(self.ventana, text="Ingresa tu nombre:", bg="spring green", font=("Arial", 12))
        label_jugador.pack(pady=10)

        self.jugador_var = tk.StringVar(self.ventana)  # Variable para almacenar el nombre del jugador
        self.validador = self.ventana.register(self.validar_entrada)  # Registrar el validador

        entry_jugador = tk.Entry(self.ventana, textvariable=self.jugador_var, validate='key', validatecommand=(self.validador, '%S'), font=("Arial", 12))
        entry_jugador.pack(pady=5)

        btn_registrar = tk.Button(self.ventana, text="Registrar", command=self.registrar_jugador, bg="#2196F3", fg="white", font=("Arial", 12, 'bold'))
        btn_registrar.pack(pady=10)

    def validar_entrada(self, entrada):
        # Verifica si la entrada es una letra
        return entrada.isalpha() or entrada == ""  # Permitir letras y el espacio vacío

    def registrar_jugador(self):
        nombre_jugador = self.jugador_var.get().strip()
        if nombre_jugador:
            try:
                self.db.registrar_jugador(nombre_jugador)  # Registra al jugador en la base de datos
                messagebox.showinfo("Registro", f"Jugador registrado: {nombre_jugador}")
                self.jugador_var.set("")  # Limpia el campo de entrada
            except mysql.connector.errors.IntegrityError:
                messagebox.showwarning("Advertencia", "Este nombre ya está registrado. Puedes iniciar sesión y jugar.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre.")

    def seleccionar_tematica(self):
        label_tematica = tk.Label(self.ventana, text="Selecciona una temática:", bg="spring green", font=("Arial", 12))
        label_tematica.pack(pady=10)

        tematicas = self.db.obtener_tematica()
        self.tematica_var = tk.StringVar(self.ventana)
        self.tematica_var.set(tematicas[0][1] if tematicas else "Ninguna")  # Valor por defecto

        dropdown_tematica = tk.OptionMenu(self.ventana, self.tematica_var, *[f"{tematica[1]}" for tematica in tematicas])
        dropdown_tematica.config(bg="maroon2", font=("Arial", 12, 'bold'))
        dropdown_tematica.pack(pady=5)

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
            messagebox.showwarning("Advertencia", "Por favor, selecciona un jugador y una temática.")

