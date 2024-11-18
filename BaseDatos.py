import mysql.connector

class BaseDatos:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pythonAhorcado"
        )

    def mostrar_estadisticas(self, jugador_id):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT ganadas, perdidas FROM jugadores WHERE id = %s", (jugador_id,))
            result = cursor.fetchone()
            if result is None:
                return (0, 0)  # Devuelve 0 si no hay estadísticas
            return result
        except mysql.connector.Error as err:
            print(f"Error al mostrar estadísticas: {err}")
            return (0, 0)  # Manejo de errores
        finally:
            cursor.close()

    def registrar_estadisticas(self, jugador_id, ganada):
        cursor = self.connection.cursor()
        if ganada:
            cursor.execute("UPDATE jugadores SET ganadas = ganadas + 1 WHERE id = %s", (jugador_id,))
        else:
            cursor.execute("UPDATE jugadores SET perdidas = perdidas + 1 WHERE id = %s", (jugador_id,))
        self.connection.commit()
        cursor.close()

    def obtener_jugadores(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, nombre FROM jugadores")
            return cursor.fetchall()  # Retorna una lista de tuplas (id, nombre)
        except mysql.connector.Error as err:
            print(f"Error al obtener jugadores: {err}")
            return []
        finally:
            cursor.close()

    def obtener_tematica(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, nombre FROM tematicas")
            return cursor.fetchall()  # Retorna una lista de tuplas (id, nombre)
        except mysql.connector.Error as err:
            print(f"Error al obtener temáticas: {err}")
            return []
        finally:
            cursor.close()

    def obtener_palabras_por_tematica(self, tematica_id):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT palabra FROM palabras WHERE tematica_id = %s", (tematica_id,))
            return [row[0] for row in cursor.fetchall()]  # Retorna una lista de palabras
        except mysql.connector.Error as err:
            print(f"Error al obtener palabras: {err}")
            return []
        finally:
            cursor.close()

    def registrar_jugador(self, nombre):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO jugadores (nombre) VALUES (%s)", (nombre,))
        self.connection.commit()
        cursor.close()

    def cerrar_conexion(self):
        self.connection.close()








