import os
import sqlite3
from typing import Any

# Definir la ruta a la base de datos
PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'src', 'backend', 'app', 'data')
DB_FILE = os.path.join(DIR_DATA, 'data.db')

class UniversalController:
    """Universal controller for CRUD operations using SQLite."""

    def __init__(self):
        """Initialize the database connection and cursor."""
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.conn.cursor()

    def _get_table_name(self, obj: Any) -> str:
        """Retrieve the table name based on the object's class."""
        if hasattr(obj, "__entity_name__"):
            return obj.__entity_name__
        elif hasattr(obj.__class__, "__entity_name__"):
            return obj.__class__.__entity_name__
        else:
            raise ValueError("El objeto o su clase no tienen definido '__entity_name__'.")

    def _ensure_table_exists(self, obj: Any):
        """Ensure that the table exists in the database; create it if it doesn't."""
        table = self._get_table_name(obj)
        fields = obj.get_fields()
        columns = ", ".join(f"{k} {v}" for k, v in fields.items())
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({columns})"
        self.cursor.execute(sql)
        self.conn.commit()
        
    def add(self, obj: Any) -> Any:
        """Add a new object to the database."""
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = list(data.values())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(
                f"An object with the same primary key already exists in '{table}'."
            )

        return obj

    def read_all(self, obj: Any) -> list[dict]:
        """Retrieve all objects from a table."""
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_by_id(self, model, id):
        """Retrieve a single record by ID."""
        self._ensure_table_exists(model)
        table = model.__entity_name__
        primary_key = list(model.get_fields().keys())[0]  # Obtener el nombre de la clave primaria
        sql = f"SELECT * FROM {table} WHERE {primary_key} = ?"
        self.cursor.execute(sql, (id,))
        row = self.cursor.fetchone()

        if not row:
            return None  # Devolver None si no se encuentra el registro

        # Convertir los datos en un diccionario compatible con el modelo
        fields = model.get_fields()
        data = {key: row[idx] for idx, key in enumerate(fields.keys())}

        return model(**data)

    def update(self, obj: Any) -> Any:
        """Update an existing object."""
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()
        id_field = list(data.keys())[0]  # Obtener el nombre de la clave primaria

        assignments = ', '.join(
            f"{k} = ?" for k in data if k != id_field
        )
        values = [v for k, v in data.items() if k != id_field]
        values.append(data[id_field])

        sql = f"UPDATE {table} SET {assignments} WHERE {id_field} = ?"
        self.cursor.execute(sql, values)
        self.conn.commit()

        if self.cursor.rowcount == 0:
            raise ValueError(f"No se encontró un registro con {id_field} = {data[id_field]} en la tabla '{table}'.")

        return obj

    def delete(self, obj: Any) -> bool:
        """Delete an object by its ID."""
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()
        id_field = list(data.keys())[0]  # Obtener el nombre de la clave primaria

        sql = f"DELETE FROM {table} WHERE {id_field} = ?"
        self.cursor.execute(sql, (data[id_field],))
        self.conn.commit()

        if self.cursor.rowcount == 0:
            raise ValueError(f"No se encontró un registro con {id_field} = {data[id_field]} en la tabla '{table}'.")
        return True

    def clear_tables(self):
        """Delete all data from all tables in the database without dropping them."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        for table in tables:
            table_name = table["name"]
            self.cursor.execute(f"DELETE FROM {table_name}")
        self.conn.commit()
    def get_by_unit(self, unit_id: int) -> list[dict]:
        sql = "SELECT * FROM mantenimiento WHERE id_unit = ?"
        self.cursor.execute(sql, (unit_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]