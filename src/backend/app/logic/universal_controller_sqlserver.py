import pyodbc
from backend.app.core.config import Settings
from typing import Any
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
class UniversalController:
    def __init__(self):
        try:
            settings = Settings()
            self.conn = pyodbc.connect(
    f"DRIVER={{SQL Server}};SERVER={settings.db_config['host']},1435;DATABASE={settings.db_config['dbname']};UID={settings.db_config['user']};PWD={settings.db_config['password']}"
)
            self.conn.autocommit = False  # Desactivar autocommit
            self.cursor = self.conn.cursor()
        except pyodbc.Error as e:
            raise ConnectionError(f"Error de conexión a la base de datos: {e}")

    def _get_table_name(self, obj: Any) -> str:
        if hasattr(obj, "__entity_name__"):
            return obj.__entity_name__
        elif hasattr(obj.__class__, "__entity_name__"):
            return obj.__class__.__entity_name__
        else:
            raise ValueError("El objeto o su clase no tienen definido '__entity_name__'.")

    def _ensure_table_exists(self, obj: Any):
        """Crea la tabla si no existe."""
        table = self._get_table_name(obj)
        fields = obj.get_fields()

        columns = []
        for k, v in fields.items():
            if k == "id":
                columns.append(f"{k} INT IDENTITY(1,1) PRIMARY KEY")
            else:
                columns.append(f"{k} {v}")

        sql = f"IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table}' AND xtype='U') CREATE TABLE {table} ({', '.join(columns)})"
        self.cursor.execute(sql)
        self.conn.commit()

    def drop_table(self, obj: Any) -> None:
        """Elimina la tabla de la base de datos."""
        table = self._get_table_name(obj)
        sql = f"IF EXISTS (SELECT * FROM sysobjects WHERE name='{table}' AND xtype='U') DROP TABLE {table}"
        self.cursor.execute(sql)
        self.conn.commit()

    def read_all(self, obj: Any) -> list[dict]:
        self._ensure_table_exists(obj)
        table = self._get_table_name(obj)
        self.cursor.execute(f"SELECT * FROM {table}")
        return [dict(zip([column[0] for  column in self.cursor.description], row)) for row in self.cursor.fetchall()]

    def get_by_id(self, cls: Any, id_value: Any) -> Any | None:
        table = cls.__entity_name__
        sql = f"SELECT * FROM {table} WHERE id = ?"
        self.cursor.execute(sql, (id_value,))
        row = self.cursor.fetchone()

        return cls.from_dict(dict(zip([column[0] for column in self.cursor.description], row))) if row else None

    def get_by_column(self, cls: Any, column_name: str, value: Any) -> Any | None:
        table = cls.__entity_name__
        sql = f"SELECT * FROM {table} WHERE {column_name} = ?"

        self.cursor.execute(sql, (value,))
        row = self.cursor.fetchone()

        return cls.from_dict(dict(zip([column[0] for column in self.cursor.description], row))) if row else None

    def add(self, obj: Any) -> Any:
        """
        Agrega un nuevo registro a la tabla correspondiente al objeto proporcionado.
        """
        table = self._get_table_name(obj)
        data = obj.to_dict()

        # Eliminar el campo ID si es None (autoincremental)
        if "ID" in data and data["ID"] is None:
            del data["ID"]

        # Construir la consulta SQL para insertar el registro
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data.values()])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            return obj
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Error al agregar el registro: {e}")

    def update(self, obj: Any) -> Any:
        """
        Actualiza un registro en la tabla correspondiente al objeto proporcionado.
        """
        table = self._get_table_name(obj)
        data = obj.to_dict()

        if "ID" not in data or data["ID"] is None:
            raise ValueError("El objeto debe tener un campo 'ID' válido para ser actualizado.")

        # Construir la consulta SQL para actualizar el registro
        columns = [f"{key} = ?" for key in data.keys() if key != "ID"]
        sql = f"UPDATE {table} SET {', '.join(columns)} WHERE ID = ?"

        try:
            # Ejecutar la consulta con los valores correspondientes
            values = [data[key] for key in data.keys() if key != "ID"] + [data["ID"]]
            self.cursor.execute(sql, values)
            self.conn.commit()
            return obj
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Error al actualizar el registro: {e}")

    def delete(self, obj: Any) -> bool:
        """
        Elimina un registro de la tabla correspondiente al objeto proporcionado.
        """
        table = self._get_table_name(obj)
        data = obj.to_dict()

        if "ID" not in data or data["ID"] is None:
            raise ValueError("El objeto debe tener un campo 'ID' válido para ser eliminado.")

        sql = f"DELETE FROM {table} WHERE ID = ?"
        try:
            # Ejecutar la consulta para eliminar el registro
            self.cursor.execute(sql, (data["ID"],))
            self.conn.commit()

            # Verificar si el registro fue eliminado
            self.cursor.execute(f"SELECT * FROM {table} WHERE ID = ?", (data["ID"],))
            if self.cursor.fetchone() is None:
                return True
            else:
                return False
        except Exception as e:
            self.conn.rollback()
            raise ValueError(f"Error al eliminar el registro: {e}")
    
    def get_by_unit(self, unit_id: int) -> list[dict]:
        sql = "SELECT * FROM mantenimiento WHERE id_unit = ?"
        try:
            self.cursor.execute(sql, (unit_id,))
            rows = self.cursor.fetchall()
            # Convertir cada fila en un diccionario utilizando los nombres de las columnas
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in rows]
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener registros de la unidad {unit_id}: {e}")
    def _execute_query(self, query: str, params: tuple = ()) -> list:
        """Ejecuta una consulta SQL y retorna los resultados como una lista de diccionarios."""
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchone()
            return rows
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al ejecutar la consulta: {e}")

    def obtener_ruta_con_interconexion(self, ubicacion_llegada: str, ubicacion_final: str) -> dict:
        response = {"interconexiones": []}  # Inicializar la respuesta en formato JSON

        try:
            # Obtener rutas desde la ubicación de llegada
            query_llegada = '''
            SELECT r.ID, r.Nombre, p.ID, p.Ubicacion
            FROM DB_PUBLIC_TRANSIT_AGENCY.dbo.Ruta r
            JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.RutaParada rp ON r.ID = rp.IDRuta
            JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.Parada p ON rp.IDParada = p.ID
            WHERE p.Ubicacion = ?;
            '''
            self.cursor.execute(query_llegada, (ubicacion_llegada,))
            rutas_llegada = self.cursor.fetchall()

            if not rutas_llegada:
                return {"mensaje": "No se encontraron rutas desde la ubicación de llegada."}

            for ruta_id, ruta_name, parada_id, parada_ubicacion in rutas_llegada:
                # Obtener rutas que lleguen a la ubicación final
                query_final = '''
                SELECT r.ID, r.Nombre, p.ID, p.Ubicacion
                FROM DB_PUBLIC_TRANSIT_AGENCY.dbo.Ruta r
                JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.RutaParada rp ON r.ID = rp.IDRuta
                JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.Parada p ON rp.IDParada = p.ID
                WHERE p.Ubicacion = ?;
                '''
                self.cursor.execute(query_final, (ubicacion_final,))
                rutas_final = self.cursor.fetchall()

                if not rutas_final:
                    return {"mensaje": "No se encontraron rutas hacia la ubicación final."}

                for ruta_final_id, ruta_final_name, parada_final_id, parada_final_ubicacion in rutas_final:
                    # Verificar interconexión entre rutas
                    query_interconexion = '''
                    SELECT p.ID, p.Ubicacion
                    FROM DB_PUBLIC_TRANSIT_AGENCY.dbo.Parada p
                    JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.RutaParada rp1 ON p.ID = rp1.IDParada
                    JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.RutaParada rp2 ON p.ID = rp2.IDParada
                    WHERE rp1.IDRuta = ? AND rp2.IDRuta = ?;
                    '''
                    self.cursor.execute(query_interconexion, (ruta_id, ruta_final_id))
                    interconexiones = self.cursor.fetchall()

                    # Procesar interconexiones encontradas
                    if interconexiones:
                        for inter_parada_id, inter_ubicacion in interconexiones:
                            response["interconexiones"].append({
                                "ruta_inicio": ruta_name,
                                "ruta_final": ruta_final_name,
                                "interconexion": inter_ubicacion
                            })
                    else:
                        response["interconexiones"].append({
                            "ruta_inicio": ruta_name,
                            "ruta_final": ruta_final_name,
                            "interconexion": "Sin interconexión directa"
                        })

            # Si no se encontró ninguna interconexión
            if not response["interconexiones"]:
                return {"mensaje": "No se encontraron rutas con interconexión."}

        except Exception as e:
            response = {"error": f"Error al obtener la ruta: {str(e)}"}
            logger.error(response["error"])
        finally:
            self.conn.commit()  # Confirmar transacción

        return response


    # Método para obtener cualquier cuenta
    def total_registros(self, table: str, condition: str = "") -> int:
        """Generar la consulta total por tabla"""
        query = f"SELECT COUNT(*) FROM {table} {condition}"
        result = self._execute_query(query)
        return result[0] if result else 0

    # Método para obtener registros de una tabla específica
    def total_movimientos(self) -> int:
        return self.total_registros('movimiento')

    def total_unidades(self) -> int:
        return self.total_registros('unidadtransporte')

    def total_pasajeros(self) -> int:
        return self.total_registros('Usuario', "WHERE IDRolUsuario = 1")

    def total_operarios(self) -> int:
        return self.total_registros('usuario', "WHERE IDRolUsuario = 2")

    def total_supervisores(self) -> int:
        return self.total_registros('usuario', "WHERE IDRolUsuario = 3")

    def total_mantenimiento(self) -> int:
        return self.total_registros('mantenimiento')

    def proximos_mantenimientos(self) -> int:
        return self.total_registros('mantenimiento', "WHERE fecha < GETDATE()")

    def alerta_mantenimiento_atrasados(self) -> list:
        return self._execute_query("SELECT * FROM mantenimiento WHERE fecha < GETDATE()")

    def alerta_mantenimiento_proximos(self) -> list:
        return self._execute_query("SELECT * FROM mantenimiento WHERE fecha BETWEEN GETDATE() AND DATEADD(DAY, 7, GETDATE())")

    def total_usuarios(self) -> int:
        return self.total_registros('usuario')

    def promedio_horas_trabajadas(self) -> float:
        query = "SELECT AVG(horastrabajadas) FROM rendimiento"
        result = self._execute_query(query)
        return result[0] if result else 0.0

    def last_card_used(self, id_card: int) -> str:
        query = """
        SELECT TOP 1 a.TipoMovimiento, m.Monto
        FROM Movimiento m
        INNER JOIN TipoMovimiento a ON m.IDTipoMovimiento = a.ID
        WHERE a.ID = ?
        ORDER BY m.ID DESC;
        """
        result = self._execute_query(query, (id_card,))
        return result[0] if result else None

    def get_ruta_parada(self, id_ruta: int = None, id_parada: int = None) -> list[dict]:
        """
        Obtiene las relaciones Ruta-Parada según el ID de Ruta, ID de Parada o todos los registros.
        """
        sql = "SELECT rp.IDRuta, rp.IDParada, r.Nombre AS NombreRuta, p.Nombre AS NombreParada " \
              "FROM RutaParada rp " \
              "JOIN Ruta r ON rp.IDRuta = r.ID " \
              "JOIN Parada p ON rp.IDParada = p.ID"

        conditions = []
        params = []

        if id_ruta:
            conditions.append("rp.IDRuta = ?")
            params.append(id_ruta)
        if id_parada:
            conditions.append("rp.IDParada = ?")
            params.append(id_parada)

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        try:
            self.cursor.execute(sql, tuple(params))
            rows = self.cursor.fetchall()
            # Convertir cada fila en un diccionario utilizando los nombres de las columnas
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in rows]
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener registros de Ruta-Parada: {e}")
