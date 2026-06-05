import sqlite3 as sq
from D&D.py import Heroe

class Database:
    def __init__(self, db_name = 'campania_dnd.db'):
        self.db_name = db_name
    
    def conectar(self):
        conexion = sq.connect(self.db_name)
        conexion.execute("PRAGMA foreign_keys = ON;")
        return conexion

class HeroeRepo:
    def __init__(self):
        self.db = Database()
    def create(self, heroe: Heroe):
        conn = self.db.conectar()
        cursor = conn.cursor()
        query = "INSERT INTO heroes (nombre, clase, raza, nivel) VALUES (?, ?. ?)"
        cursor.execute(query, (heroe.nombre, heroe.clase, heroe.raza, heroe.nivel))
        conn.commit()
        heroe.id = cursor.lastrowid
        conn.close
