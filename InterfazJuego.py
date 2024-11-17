import tkinter as tk
from tkinter import messagebox

class InterfazJuego:
    def __init__(self, root, db, juego):
        self.db = db
        self.juego = juego

        self.root = root
        self.root.title("Juego del Ahorcado")

        self.temas = self.db.obtener_tematicas()
        self.tema_var = tk.StringVar(value=self.temas[0])
        tk.Label(root, text="Elige una temática:").pack()
        for tema in self.temas:
            tk.Radiobutton(root, text=tema, variable=self.tema_var, value=tema).pack()

        self.jugador_var = tk.StringVar()
        tk.Label(root, text="Nombre del jugador:").pack()
        tk.Entry(root, textvariable=self.jugador_var).pack()

        tk.Button(root, text="Iniciar Juego", command=self.iniciar_juego).pack()

    def iniciar_juego(self):
        tema = self.tema_var.get()
        jugador = self.jugador_var.get().strip()
        if not jugador:
            messagebox.showerror("Error", "Por favor, ingresa un nombre de jugador.")
            return

        self.db.guardar_jugador(jugador)
        self.juego.seleccionar_palabra(tema)

        self.ventana_juego = tk.Toplevel(self.root)
        self.ventana_juego.title("Adivina la palabra")

        self.palabra_label = tk.Label(self.ventana_juego, text=" ".join(self.juego.letras_adivinadas))
        self.palabra_label.pack()

        self.letra_var = tk.StringVar()
        tk.Entry(self.ventana_juego, textvariable=self.letra_var).pack()
        tk.Button(self.ventana_juego, text="Adivinar", command=self.adivinar_letra).pack()

        self.intentos_label = tk.Label(self.ventana_juego, text=f"Intentos restantes: {self.juego.intentos}")
        self.intentos_label.pack()

        self.jugador = jugador

    def adivinar_letra(self):
        letra = self.letra_var.get().strip()
        if letra and len(letra) == 1:
            correcto = self.juego.adivinar_letra(letra.lower())
            self.palabra_label.config(text=" ".join(self.juego.letras_adivinadas))
            self.intentos_label.config(text=f"Intentos restantes: {self.juego.intentos}")

            if self.juego.juego_terminado():
                if self.juego.es_ganador():
                    messagebox.showinfo("Resultado", "¡Ganaste!")
                    self.db.actualizar_estadisticas(self.jugador, 1, 0)
                else:
                    messagebox.showinfo("Resultado", "Perdiste...")
                    self.db.actualizar_estadisticas(self.jugador, 0, 1)
                self.ventana_juego.destroy()
