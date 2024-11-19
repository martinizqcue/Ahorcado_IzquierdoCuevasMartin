import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class InterfazJuego:
    def __init__(self, ventana, db, jugador, tematica_data):
        self.ventana = ventana
        self.db = db
        self.jugador = jugador
        self.tematica_data = tematica_data
        self.palabra = ''
        self.intentos = 6
        self.letras_adivinadas = []
        self.letras_usadas = []  # Lista para almacenar letras usadas

        # Cargar imágenes desde monigote0.png hasta monigote6.png
        try:
            self.imagenes = [ImageTk.PhotoImage(Image.open(f'Imagenes/monigote{i}.png')) for i in range(7)]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las imágenes: {e}")

        self.ventana.title("Juego del Ahorcado")

        self.centrar_ventana()
        self.ventana.resizable(False, False)  # Desactivar maximizar
        self.ventana.configure(bg="cyan2")  # Color de fondo

        self.imagen_label = tk.Label(self.ventana, bg="purple4")  # Label para mostrar la imagen
        self.imagen_label.pack(pady=10)

        self.crear_interfaz()

    def centrar_ventana(self):
        # Obtener el tamaño de la pantalla
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()

        # Obtener el tamaño de la ventana
        ancho_ventana = 700
        alto_ventana = 700

        # Calcular la posición x, y para centrar la ventana
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        # Colocar la ventana en la posición calculada
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    def crear_interfaz(self):
        jugador_id = self.jugador[0]
        stats = self.db.mostrar_estadisticas(jugador_id)

        ganadas, perdidas = stats
        label_estadisticas = tk.Label(self.ventana, text=f"Ganadas: {ganadas}, Perdidas: {perdidas}", bg="gold", font=("Arial", 12, 'bold'))
        label_estadisticas.pack(pady=5)

        label_titulo = tk.Label(self.ventana, text="¡Bienvenido al Juego del Ahorcado!", bg="SeaGreen1", fg="black", font=("Arial", 16, 'bold'))
        label_titulo.pack(pady=10)

        self.label_letras_usadas = tk.Label(self.ventana, text="Letras usadas: ",fg="white", bg="magenta4", font=("Arial", 12, 'bold'))
        self.label_letras_usadas.pack(pady=5)

        self.label_palabra = tk.Label(self.ventana, text="", bg="lemon chiffon", font=("Arial", 14))
        self.label_palabra.pack(pady=10)

        self.entry_letra = tk.Entry(self.ventana, font=("Arial", 14), justify='center')
        self.entry_letra.pack(pady=5)

        btn_adivinar = tk.Button(self.ventana, text="Adivinar Letra", command=self.adivinar_letra, bg="deep pink", fg="black", font=("Arial", 12, 'bold'))
        btn_adivinar.pack(pady=10)

        self.label_intentos = tk.Label(self.ventana, text=f"Intentos restantes: {self.intentos}", bg="red",fg="white", font=("Arial", 12, 'bold'))
        self.label_intentos.pack(pady=5)


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

        if letra in self.letras_usadas or len(letra) != 1 or not letra.isalpha():
            messagebox.showwarning("Advertencia", "Letra ya adivinada o entrada inválida.")
            return

        self.letras_usadas.append(letra)  # Agregar letra a las letras usadas
        self.label_letras_usadas.config(text=f"Letras usadas: {', '.join(self.letras_usadas)}")  # Actualizar la etiqueta

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

