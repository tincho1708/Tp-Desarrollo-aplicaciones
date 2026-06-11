import sqlite3

class Heroe:
    def __init__(self, nombre, nivel, clase, raza, id):
        self.nombre = nombre
        self.nivel = nivel
        self.clase = clase
        self.raza = raza
        self.id = id
        self.bonificador_ataque = self.nivel * 0.2

    def __str__(self):
        return f" Nombre {self.nombre} | Nivel {self.nivel} | Clase {self.clase} | Raza {self.raza} | Bonificador de Ataque {self.bonificador_ataque}"


class Tesoro:
    def __init__(self, nombre_item, tipo, rareza):
        self.nombre_item = nombre_item
        self.tipo = tipo
        self.rareza = rareza
        
    def __str__(self):
        return f" Item {self.nombre_item} | Tipo {self.tipo} | Rareza {self.rareza}"


class Mazmorra:
    def __init__(self, nombre_lugar, nivel_mazmorra, enemigo_final, fue_completada):
        self.nombre_lugar = nombre_lugar
        self.nivel_mazmorra = nivel_mazmorra
        self.enemigo_final = enemigo_final
        self.fue_completada = fue_completada

    def es_letal_para(self, heroe: Heroe):
        return self.nivel_mazmorra - heroe.nivel >= 5


    def __str__(self):
        return f" Lugar {self.nombre_lugar} | Dificultad {self.nivel_mazmorra} | Enemigo Final {self.enemigo_final}"