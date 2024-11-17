import random


class JuegoAhorcado:
    def __init__(self, db):
        self.db = db
        self.palabra = ""
        self.intentos = 6
        self.letras_adivinadas = []

    def seleccionar_palabra(self, tema):
        palabras = self.db.obtener_palabras_por_tematica(tema)
        self.palabra = random.choice(palabras)
        self.letras_adivinadas = ["_" for _ in self.palabra]

    def adivinar_letra(self, letra):
        acierto = False
        for i, l in enumerate(self.palabra):
            if l == letra:
                self.letras_adivinadas[i] = letra
                acierto = True
        if not acierto:
            self.intentos -= 1
        return acierto

    def juego_terminado(self):
        return self.intentos == 0 or "_" not in self.letras_adivinadas

    def es_ganador(self):
        return "_" not in self.letras_adivinadas
