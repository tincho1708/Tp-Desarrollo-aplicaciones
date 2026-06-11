import sqlite3 as sq
import importlib.util
import os

# D&D.py tiene & en el nombre, no se puede importar con import normal
_base = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("DnD", os.path.join(_base, "D&D.py"))
_mod  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
Heroe    = _mod.Heroe
Tesoro   = _mod.Tesoro
Mazmorra = _mod.Mazmorra


class Database:
    def __init__(self, db_name="campania_dnd.db"):
        self.db_name = os.path.join(_base, db_name)

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
        cursor.execute(
            "INSERT INTO heroes (nombre, clase, raza, nivel) VALUES (?, ?, ?, ?)",
            (heroe.nombre, heroe.clase, heroe.raza, heroe.nivel)
        )
        conn.commit()
        heroe.id = cursor.lastrowid
        conn.close()

    def selectAll(self, clase=None):
        conn = self.db.conectar()
        cursor = conn.cursor()
        if clase:
            cursor.execute("SELECT * FROM heroes WHERE clase = ?", (clase,))
        else:
            cursor.execute("SELECT * FROM heroes")
        rows = cursor.fetchall()
        conn.close()
        return [Heroe(nombre=r[1], nivel=r[4], clase=r[2], raza=r[3], id=r[0]) for r in rows]

    def selectById(self, hid: int):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM heroes WHERE id = ?", (hid,))
        r = cursor.fetchone()
        conn.close()
        if r:
            return Heroe(nombre=r[1], nivel=r[4], clase=r[2], raza=r[3], id=r[0])
        return None

    def update(self, heroe: Heroe):
        conn = self.db.conectar()
        conn.execute(
            "UPDATE heroes SET nombre = ?, clase = ?, raza = ?, nivel = ? WHERE id = ?",
            (heroe.nombre, heroe.clase, heroe.raza, heroe.nivel, heroe.id)
        )
        conn.commit()
        conn.close()

    def subirNivel(self, hid: int, cantidad: int = 1):
        conn = self.db.conectar()
        conn.execute(
            "UPDATE heroes SET nivel = MIN(nivel + ?, 20) WHERE id = ?",
            (cantidad, hid)
        )
        conn.commit()
        conn.close()

    def delete(self, hid: int):
        conn = self.db.conectar()
        conn.execute("DELETE FROM heroes WHERE id = ?", (hid,))
        conn.commit()
        conn.close()


class TesoroRepo:
    def __init__(self):
        self.db = Database()

    def create(self, tesoro: Tesoro, id_propietario=None):
        conn = self.db.conectar()
        conn.execute(
            "INSERT INTO tesoros (nombre_item, tipo, rareza, id_propietario) VALUES (?, ?, ?, ?)",
            (tesoro.nombre_item, tesoro.tipo, tesoro.rareza, id_propietario)
        )
        conn.commit()
        conn.close()

    def selectAll(self, rareza=None):
        conn = self.db.conectar()
        cursor = conn.cursor()
        query = """SELECT t.id, t.nombre_item, t.tipo, t.rareza,
                          COALESCE(h.nombre, 'Sin portador')
                   FROM tesoros t LEFT JOIN heroes h ON t.id_propietario = h.id"""
        if rareza:
            cursor.execute(query + " WHERE t.rareza = ?", (rareza,))
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete(self, tid: int):
        conn = self.db.conectar()
        conn.execute("DELETE FROM tesoros WHERE id = ?", (tid,))
        conn.commit()
        conn.close()


class MazmorrasRepo:
    def __init__(self):
        self.db = Database()

    def create(self, mazmorra_nombre: str, dificultad: int, enemigo_final: str):
        conn = self.db.conectar()
        conn.execute(
            "INSERT INTO mazmorras (nombre_lugar, dificultad, enemigo_final, fue_completada) VALUES (?, ?, ?, 0)",
            (mazmorra_nombre, dificultad, enemigo_final)
        )
        conn.commit()
        conn.close()

    def selectAll(self):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mazmorras ORDER BY fue_completada, dificultad")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def toggleCompletada(self, mid: int, estado: int):
        conn = self.db.conectar()
        conn.execute("UPDATE mazmorras SET fue_completada = ? WHERE id = ?", (estado, mid))
        conn.commit()
        conn.close()

    def delete(self, mid: int):
        conn = self.db.conectar()
        conn.execute("DELETE FROM mazmorras WHERE id = ?", (mid,))
        conn.commit()
        conn.close()


def init_db():
    db = Database()
    conn = db.conectar()
    conn.execute('''CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL, clase TEXT, raza TEXT, nivel INTEGER)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS tesoros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_item TEXT NOT NULL, tipo TEXT, rareza TEXT, id_propietario INTEGER,
        FOREIGN KEY (id_propietario) REFERENCES heroes(id))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS mazmorras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_lugar TEXT NOT NULL, dificultad INTEGER,
        enemigo_final TEXT, fue_completada INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()
