import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image,ImageTk


class InterfazJuego:
    def __init__(self, ventana, db, jugador, tematica_data):
        self.ventana = ventana
        self.db = db
        self.jugador = jugador
        self.tematica_data = tematica_data
        self.palabra = ''
        self.intentos = 6
        self.letras_adivinadas = []

        # Cargar imágenes desde monigote0.png hasta monigote6.png
        self.imagenes = [ImageTk.PhotoImage(Image.open(f'monigote{i}.png')) for i in range(7)]

        self.imagen_label = tk.Label(self.ventana)  # Label para mostrar la imagen
        self.imagen_label.pack()

        self.crear_interfaz()

    def crear_interfaz(self):
        jugador_id = self.jugador[0]
        stats = self.db.mostrar_estadisticas(jugador_id)

        ganadas, perdidas = stats
        label_estadisticas = tk.Label(self.ventana, text=f"Ganadas: {ganadas}, Perdidas: {perdidas}")
        label_estadisticas.pack()

        label_titulo = tk.Label(self.ventana, text="¡Bienvenido al Juego del Ahorcado!")
        label_titulo.pack()

        self.label_palabra = tk.Label(self.ventana, text="")
        self.label_palabra.pack()

        self.entry_letra = tk.Entry(self.ventana)
        self.entry_letra.pack()

        btn_adivinar = tk.Button(self.ventana, text="Adivinar Letra", command=self.adivinar_letra)
        btn_adivinar.pack()

        self.label_intentos = tk.Label(self.ventana, text=f"Intentos restantes: {self.intentos}")
        self.label_intentos.pack()

        self.iniciar_juego()

    def iniciar_juego(self):
        palabras = self.db.obtener_palabras_por_tematica(self.tematica_data['id'])
        if not palabras:
            messagebox.showerror("Error", "No hay palabras disponibles para esta temática.")
            self.ventana.destroy()
            return

        self.palabra = random.choice(palabras)
        self.letras_adivinadas = ['_'] * len(self.palabra)
        self.actualizar_palabra()

    def actualizar_palabra(self):
        self.label_palabra.config(text=' '.join(self.letras_adivinadas))
        self.imagen_label.config(image=self.imagenes[6 - self.intentos])  # Mostrar imagen correspondiente

    def adivinar_letra(self):
        letra = self.entry_letra.get().lower()
        self.entry_letra.delete(0, tk.END)

        if letra in self.letras_adivinadas or len(letra) != 1:
            messagebox.showwarning("Advertencia", "Letra ya adivinada o entrada inválida.")
            return

        if letra in self.palabra:
            for index, char in enumerate(self.palabra):
                if char == letra:
                    self.letras_adivinadas[index] = letra
            self.actualizar_palabra()
            if '_' not in self.letras_adivinadas:
                messagebox.showinfo("¡Ganaste!", "¡Felicidades! Has adivinado la palabra.")
                self.finalizar_juego(True)
                self.ventana.destroy()
        else:
            self.intentos -= 1
            self.label_intentos.config(text=f"Intentos restantes: {self.intentos}")
            self.actualizar_palabra()  # Actualiza la imagen también
            if self.intentos == 0:
                messagebox.showerror("Perdiste", f"Has perdido. La palabra era: {self.palabra}")
                self.finalizar_juego(False)
                self.ventana.destroy()

    def finalizar_juego(self, ganada):
        self.db.registrar_estadisticas(self.jugador[0], ganada)





