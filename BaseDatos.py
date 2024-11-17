import mysql.connector
import random

class BaseDatos:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pythonAhorcado"
        )
        self.cursor = self.conexion.cursor()

    def obtener_tematicas(self):
        query = "SELECT nombre FROM tematicas"
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def obtener_palabras_por_tematica(self, tematica):
        query = """
        SELECT p.palabra
        FROM palabras p
        JOIN tematicas t ON p.tematica_id = t.id
        WHERE t.nombre = %s
        """
        self.cursor.execute(query, (tematica,))
        return [row[0] for row in self.cursor.fetchall()]

    def guardar_jugador(self, nombre):
        try:
            query = "INSERT INTO jugadores (nombre) VALUES (%s)"
            self.cursor.execute(query, (nombre,))
            self.conexion.commit()
        except mysql.connector.errors.IntegrityError:
            pass  # Si el jugador ya existe, lo ignoramos

    def actualizar_estadisticas(self, nombre, ganadas, perdidas):
        self.guardar_jugador(nombre)
        query = """
        INSERT INTO estadisticas (jugador_id, ganadas, perdidas)
        VALUES (
            (SELECT id FROM jugadores WHERE nombre = %s),
            %s, %s
        )
        ON DUPLICATE KEY UPDATE
            ganadas = ganadas + VALUES(ganadas),
            perdidas = perdidas + VALUES(perdidas)
        """
        self.cursor.execute(query, (nombre, ganadas, perdidas))
        self.conexion.commit()
