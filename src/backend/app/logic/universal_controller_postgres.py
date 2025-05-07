"""import os
import psycopg2
import psycopg2.extras
from backend.app.core.config import Settings
from typing import Any


class UniversalController:
    def __init__(self):
        try:
            settings = Settings()
            self.conn = psycopg2.connect(**settings.db_config)
            self.conn.autocommit = False  # Desactivar autocommit
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.Error as e:
            raise ConnectionError(f"Error de conexión a la base de datos: {e}")

    def _get_table_name(self, obj: Any) -> str:
        if hasattr(obj, "__entity_name__"):
            return obj.__entity_name__
        elif hasattr(obj.__class__, "__entity_name__"):
            return obj.__class__.__entity_name__
        else:
            raise ValueError("El objeto o su clase no tienen definido '__entity_name__'.")

    def _ensure_table_exists(self, obj: Any):
        #Crea la tabla si no existe, permitiendo que algunas tengan SERIAL en su clave primaria.
        table = self._get_table_name(obj)
        fields = obj.get_fields()

        # Define qué tablas necesitan que su clave primaria sea SERIAL
        tables_with_serial = {"tabla_con_serial_1", "tabla_con_serial_2"}

        columns = []
        for k, v in fields.items():
            if k == "id" and table in tables_with_serial:
                columns.append(f"{k} SERIAL PRIMARY KEY")
            else:
                columns.append(f"{k} {v}")

        sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})"
        self.cursor.execute(sql)
        self.conn.commit()

    def drop_table(self, obj: Any) -> None:
        #Elimina la tabla de la base de datos (solo para desarrollo).
        table = self._get_table_name(obj)
        sql = f'DROP TABLE IF EXISTS "{table}" CASCADE'
        self.cursor.execute(sql)
        self.conn.commit()


    def read_all(self, obj: Any) -> list[dict]:
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()

    def get_by_id(self, cls: Any, id_value: Any) -> Any | None:
        table = cls.__entity_name__
        id_field = "id"  # Cambia esto si el campo clave primaria tiene otro nombre específico.

        sql = f"SELECT * FROM {table} WHERE {id_field} = %s"
        self.cursor.execute(sql, (id_value,))
        row = self.cursor.fetchone()

        return cls.from_dict(dict(row)) if row else None
    
    def get_by_column(self, cls: Any, column_name: str, value: Any) -> Any | None:
        table = cls.__entity_name__
        sql = f"SELECT * FROM {table} WHERE {column_name} = %s"
        
        self.cursor.execute(sql, (value,))
        row = self.cursor.fetchone()
        
        return cls.from_dict(dict(row)) if row else None

    def add(self, obj: Any) -> Any:
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        data = obj.to_dict()

        # Verificar si la tabla usa SERIAL en el ID
        tables_with_serial = {"tabla_con_serial_1", "tabla_con_serial_2"}
        if table in tables_with_serial:
            data.pop("id", None)  # No incluir el ID si es SERIAL

        # Validar que haya datos antes de hacer el INSERT
        if not data:
            raise ValueError(f"No hay datos válidos para insertar en '{table}'")

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"
        try:
            self.cursor.execute(sql, values)

            # Solo recuperar ID si la tabla usa SERIAL
            if table in tables_with_serial:
                result = self.cursor.fetchone()
                if result and "id" in result:
                    obj.id = result["id"]

            self.conn.commit()
        except psycopg2.IntegrityError:
            self.conn.rollback()
            raise ValueError(f"Ya existe un objeto con la misma clave primaria en '{table}'.")
        except psycopg2.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Error general al insertar datos en '{table}': {e}")

        return obj


    def update(self, obj: Any) -> Any:
        table = self._get_table_name(obj)
        data = obj.to_dict()
        id_field = "id"

        if id_field not in data:
            raise ValueError(f"El objeto no tiene un campo '{id_field}'.")

        # Evitar actualizar el ID si la tabla usa SERIAL
        tables_with_serial = {"tabla_con_serial_1", "tabla_con_serial_2"}
        assignments = ', '.join(f"{k} = %s" for k in data if k != id_field)
        values = [v for k, v in data.items() if k != id_field]
        values.append(data[id_field])

        sql = f"UPDATE {table} SET {assignments} WHERE {id_field} = %s"
        self.cursor.execute(sql, values)
        self.conn.commit()
        return obj


    def delete(self, obj: Any) -> bool:
        table = self._get_table_name(obj)
        data = obj.to_dict()
        id_field = "id"

        if id_field not in data:
            raise ValueError(f"El objeto no tiene un campo '{id_field}'.")

        sql = f"DELETE FROM {table} WHERE {id_field} = %s"
        self.cursor.execute(sql, (data[id_field],))
        self.conn.commit()
        return True




    def clear_tables(self):
        #Vacía todas las tablas del esquema público
        self.cursor.execute(
            #SELECT tablename FROM pg_tables 
            #WHERE schemaname = 'public'
        )
        tables = self.cursor.fetchall()
        for table in tables:
            self.cursor.execute(f'DELETE FROM {table["tablename"]}')

    def get_by_unit(self, unit_id: int) -> list[dict]:
        sql = "SELECT * FROM mantenimiento WHERE id_unit = %s"
        self.cursor.execute(sql, (unit_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]"""