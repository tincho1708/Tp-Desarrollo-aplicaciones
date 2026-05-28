import sqlite3

class Heroe:
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel

    def __str__(self):
        return f" Nombre {self.nombre} | Nivel {self.nivel}"


class Tesoro:
    def __init__(self, nombre_item, tipo, rareza):
        self.nombre_item = nombre_item
        self.tipo = tipo
        self.rareza = rareza

    def __str__(self):
        return f" Item {self.nombre_item} | Tipo {self.tipo} | Rareza {self.rareza}"


class Mazmorra:
    def __init__(self, nombre_lugar, dificultad, enemigo_final, fue_completada):
        self.nombre_lugar = nombre_lugar
        self.dificultad = dificultad
        self.enemigo_final = enemigo_final
        self.fue_completada = fue_completada

    def __str__(self):
        return f" Lugar {self.nombre_lugar} | Dificultad {self.dificultad} | Enemigo Final {self.enemigo_final}"