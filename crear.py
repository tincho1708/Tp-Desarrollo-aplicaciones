Heroe = {}
cant_heroes = int(input("Cantidad de heroes a ingresar: "))

for i in range(cant_heroes):

    nombre = input("Nombre Heroe: ")
    clase = input("Clase de Heroe: ")
    raza = input("Raza de Heroe: ")
    nivel = input("Nivel de Heroe: ")

    heroes = {
        "nombre": nombre,
        "clase": clase,
        "raza": raza,
        "nivel": nivel
    }


