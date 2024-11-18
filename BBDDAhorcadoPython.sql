DROP DATABASE IF EXISTS pythonAhorcado;
CREATE DATABASE IF NOT EXISTS pythonAhorcado;
USE pythonAhorcado;

CREATE TABLE jugadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    ganadas INT DEFAULT 0,
    perdidas INT DEFAULT 0
);

CREATE TABLE tematicas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE palabras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    palabra VARCHAR(50) NOT NULL,
    tematica_id INT NOT NULL,
    FOREIGN KEY (tematica_id) REFERENCES tematicas(id)
);

INSERT INTO tematicas (nombre) VALUES ('frutas'), ('conceptos informáticos'), ('nombres de personas');

INSERT INTO palabras (palabra, tematica_id) VALUES
('manzana', 1), ('pera', 1), ('platano', 1), ('fresa', 1),
('variable', 2), ('funcion', 2), ('clase', 2), ('bucle', 2),
('andrea', 3), ('mario', 3), ('carla', 3), ('pablo', 3);

