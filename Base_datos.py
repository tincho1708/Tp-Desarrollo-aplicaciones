import sqlite3

def crear_base_dnd():
    # Conexión (si no existe, se crea el archivo)
    conexion = sqlite3.connect('campania_dnd.db')
    cursor = conexion.cursor()

    # 1. Tabla de HÉROES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            clase TEXT, -- Guerrero, Mago, Clerigo, Picaro
            raza TEXT, -- Humano, Elfo, Enano, Mediano
            nivel INTEGER
        )
    ''')

    # 2. Tabla de TESOROS (Relacionada con Héroes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tesoros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_item TEXT NOT NULL,
            tipo TEXT, -- Arma, Pocion, Pergamino, Armadura
            rareza TEXT, -- Comun, Raro, Legendario
            id_propietario INTEGER,
            FOREIGN KEY (id_propietario) REFERENCES heroes (id)
        )
    ''')

    # 3. Tabla de MAZMORRAS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mazmorras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_lugar TEXT NOT NULL,
            dificultad INTEGER, -- Nivel sugerido de 1 a 20
            enemigo_final TEXT,
            fue_completada INTEGER -- 1 para Sí, 0 para No
        )
    ''')

    # Datos de ejemplo iniciales
    heroes_iniciales = [
        ('Aelar', 'Mago', 'Elfo', 5),
        ('Bruenor', 'Guerrero', 'Enano', 6),
        ('Vax', 'Picaro', 'Mediano', 5)
    ]
    
    cursor.executemany('INSERT INTO heroes (nombre, clase, raza, nivel) VALUES (?, ?, ?, ?)', heroes_iniciales)

    # Objeto mágico asignado al primer héroe (Aelar)
    cursor.execute('INSERT INTO tesoros (nombre_item, tipo, rareza, id_propietario) VALUES (?, ?, ?, ?)', 
                   ('Bastón de Fuego', 'Arma', 'Raro', 1))

    conexion.commit()
    conexion.close()
    print("Base de datos 'campania_dnd.db' creada exitosamente.")

if __name__ == "__main__":
    crear_base_dnd()
