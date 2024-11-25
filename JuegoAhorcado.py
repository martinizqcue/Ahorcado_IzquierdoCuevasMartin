import random

class JuegoAhorcado:
    def __init__(self, db, jugador, tematica):
        self.db = db
        self.jugador = jugador
        self.tematica = tematica
        self.palabra = ""
        self.intentos = 6
        self.letras_adivinadas = []
        self.guardar_palabra()

    def guardar_palabra(self):
        palabras = self.db.obtener_palabras_por_tematica(self.tematica['id'])
        if palabras:
            self.palabra = random.choice(palabras)  # Seleccionar una palabra aleatoria
        else:
            print("No hay palabras disponibles para esta temática.")

    def adivinar_letra(self, letra):
        if letra in self.palabra and letra not in self.letras_adivinadas:
            self.letras_adivinadas.append(letra)
            return True
        elif letra not in self.palabra:
            self.intentos -= 1
        return False

    def palabra_completa(self):
        return all(letra in self.letras_adivinadas for letra in self.palabra)

    def estado_juego(self):
        palabra_oculta = ''.join([letra if letra in self.letras_adivinadas else '_' for letra in self.palabra])
        return palabra_oculta, self.intentos

    def finalizar_juego(self, ganada):
        self.db.registrar_estadisticas(self.jugador[0], ganada)


