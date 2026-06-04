import sqlite3 as sq

class Database:
    def __init__(self, db_name = "dnd.db")
        self.db_name = db_name
    def crear_base_dnd(Self):
        conexion = sq.connect(Self.db_name)