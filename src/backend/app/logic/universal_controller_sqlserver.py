import pyodbc
from backend.app.core.config import Settings
from typing import Any
import os
import logging
import platform
from typing import List
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
class UniversalController:
    def __init__(self):
        try:
            settings = Settings()
            # Detectar si está en un entorno Railway o local
            is_railway = os.getenv("RAILWAY_ENV", "false") == "true"

            # Detectar sistema operativo
            if is_railway or platform.system().lower() != "windows":
                driver = "ODBC Driver 18 for SQL Server"
            else:
                driver = "SQL Server"
            db_password = os.getenv('PASSWORD')
            if db_password is None:
                raise ValueError("La variable de entorno DB_PASSWORD no está definida.")
            
            self.conn = pyodbc.connect(
                f"DRIVER={{{driver}}};SERVER={settings.db_config['host']},1435;DATABASE={settings.db_config['dbname']};UID={settings.db_config['user']};PWD={db_password};TrustServerCertificate=yes"
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

    def execute_queryRutaParada(self, query: str, params: tuple = None) -> List[dict]:
        """
        Ejecuta una consulta SQL y retorna los resultados como una lista de diccionarios.
        """
        try:
            if not self.cursor:
                raise RuntimeError("El cursor de la base de datos no está disponible.")
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            rows = self.cursor.fetchall()  # Recupera todos los registros
            return [dict(zip([column[0] for column in self.cursor.description], row)) for row in rows]
        except pyodbc.Error as e:
            logger.error(f"Error al ejecutar la consulta: {e}")
            raise RuntimeError(f"Error al ejecutar la consulta: {e}")

    def get_all_rutaparada(self) -> List[dict]:
        """
        Obtiene todos los registros de la tabla RutaParada.
        """
        try:
            query = "SELECT * FROM RutaParada"
            results = self.execute_queryRutaParada(query)
            if not results:
                logger.warning("No se encontraron registros en la tabla RutaParada.")
            logger.info(f"Se obtuvieron {len(results)} registros de la tabla RutaParada.")
            return results
        except Exception as e:
            logger.error(f"Error al obtener todos los registros de RutaParada: {e}")
            raise RuntimeError(f"Error al obtener todos los registros de RutaParada: {e}")

    def get_by_id_parada(self, id_parada: int) -> List[dict]:
        """
        Obtiene registros de la tabla RutaParada filtrados por IDParada.
        """
        try:
            query = "SELECT * FROM RutaParada WHERE IDParada = ?"
            results = self.execute_queryRutaParada(query, (id_parada,))
            if not results:
                logger.warning(f"No se encontraron registros en RutaParada con IDParada={id_parada}.")
            logger.info(f"Se obtuvieron {len(results)} registros de RutaParada con IDParada={id_parada}.")
            return results
        except Exception as e:
            logger.error(f"Error al obtener registros de RutaParada por IDParada={id_parada}: {e}")
            raise RuntimeError(f"Error al obtener registros de RutaParada por IDParada={id_parada}: {e}")
    
    def _ensure_table_exists(self, obj: Any):
            """Crea la tabla si no existe."""
            table = self._get_table_name(obj)
            fields = obj.get_fields()

            columns = []
            for k, v in fields.items():
                if k == "id":
                    columns.append(f"{k} INT PRIMARY KEY")
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
        try:
            self.cursor.execute(sql, (id_value,))
            row = self.cursor.fetchone()
            return cls.from_dict(dict(zip([column[0] for column in self.cursor.description], row))) if row else None
        except Exception as e:
            logger.error(f"Error en get_by_id: {e}")
            return None

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
    
    def get_by_unit(self,cls: Any, unit_id: int) -> list[dict]:
        table= table = cls.__entity_name__
        sql = f"SELECT * FROM {table} WHERE idunidad = ?"
        try:
            self.cursor.execute(sql, (unit_id,))
            row = self.cursor.fetchone()
            return cls.from_dict(dict(zip([column[0] for column in self.cursor.description], row))) if row else None

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

    def ruta_interconexion(self, ubicacion_llegada: str, ubicacion_final: str) -> dict:
        response = {"interconexiones": []}
        try:
            rutas_llegada = self._get_rutas_por_ubicacion(ubicacion_llegada)
            if not rutas_llegada:
                return {"mensaje": "No se encontraron rutas desde la ubicación de llegada."}
            rutas_final = self._get_rutas_por_ubicacion(ubicacion_final)
            if not rutas_final:
                return {"mensaje": "No se encontraron rutas hacia la ubicación final."}
            for ruta_id, ruta_name, _, _ in rutas_llegada:
                for ruta_final_id, ruta_final_name, _, _ in rutas_final:
                    self._agregar_interconexiones(response, ruta_id, ruta_name, ruta_final_id, ruta_final_name)
            if not response["interconexiones"]:
                return {"mensaje": "No se encontraron rutas con interconexión."}
        except Exception as e:
            response = {"error": f"Error al obtener la ruta: {str(e)}"}
            logger.error(response["error"])
        finally:
            self.conn.commit()
        return response

    def _get_rutas_por_ubicacion(self, ubicacion: str):
        query = '''
        SELECT r.ID, r.Nombre, p.ID, p.Ubicacion
        FROM DB_PUBLIC_TRANSIT_AGENCY.dbo.Rutas r
        JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.RutaParada rp ON r.ID = rp.IDRuta
        JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.Parada p ON rp.IDParada = p.ID
        WHERE p.Ubicacion = ?;
        '''
        self.cursor.execute(query, (ubicacion,))
        return self.cursor.fetchall()

    def _agregar_interconexiones(self, response, ruta_id, ruta_name, ruta_final_id, ruta_final_name):
        query_interconexion = '''
        SELECT p.ID, p.Ubicacion
        FROM DB_PUBLIC_TRANSIT_AGENCY.dbo.Parada p
        JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.RutaParada rp1 ON p.ID = rp1.IDParada
        JOIN DB_PUBLIC_TRANSIT_AGENCY.dbo.RutaParada rp2 ON p.ID = rp2.IDParada
        WHERE rp1.IDRuta = ? AND rp2.IDRuta = ?;
        '''
        self.cursor.execute(query_interconexion, (ruta_id, ruta_final_id))
        interconexiones = self.cursor.fetchall()
        if interconexiones:
            for _, inter_ubicacion in interconexiones:
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
        return self.total_registros('mantenimientoins')

    def proximos_mantenimientos(self) -> int:
        return self.total_registros('mantenimientoins', "WHERE fecha < GETDATE()")

    def alerta_mantenimiento_atrasados(self) -> list:
        return self._execute_query("SELECT * FROM mantenimientoins WHERE fecha < GETDATE()")

    def alerta_mantenimiento_proximos(self) -> list:
        return self._execute_query("SELECT * FROM mantenimientoins WHERE fecha BETWEEN GETDATE() AND DATEADD(DAY, 7, GETDATE())")

    def total_usuarios(self) -> int:
        return self.total_registros('usuario')

    def promedio_horas_trabajadas(self) -> float:
        query = "SELECT AVG(horastrabajadas) FROM rendimiento"
        result = self._execute_query(query)
        return result[0] if result else 0.0

    def last_card_used(self, user_id: int) -> dict:
        """
        Retorna el último uso de tarjeta del usuario como un dict con 'tipo' y 'monto'.
        """
        query = """
SELECT TOP 1
    tm.TipoMovimiento,
    m.Monto
FROM 
    Pago p
INNER JOIN Movimiento m ON p.IDMovimiento = m.ID
INNER JOIN TipoMovimiento tm ON m.IDTipoMovimiento = tm.ID
INNER JOIN Tarjeta t ON p.IDTarjeta = t.ID
WHERE 
    t.IDUsuario = ?
ORDER BY 
    m.ID DESC;
        """
        try:
            self.cursor.execute(query, (user_id,))
            row = self.cursor.fetchone()
            if row:
                return {"tipo": row[0], "monto": row[1]}
            else:
                return {"tipo": "N/A", "monto": "N/A"}
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener el último uso de tarjeta del usuario con ID {user_id}: {e}")

    def get_ruta_parada(self, id_ruta: int = None, id_parada: int = None) -> list[dict]:
        """
        Obtiene las relaciones Ruta-Parada según el ID de Ruta, ID de Parada o todos los registros.
        """
        sql = "SELECT rp.IDRuta, rp.IDParada, r.Nombre AS NombreRuta, p.Nombre AS NombreParada " \
              "FROM RutaParada rp " \
              "JOIN Rutas r ON rp.IDRuta = r.ID " \
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
    def get_turno_usuario(self, user_id: int) -> dict:
        """
        Obtiene el turno de un usuario según su ID.
        """
        query = """
        SELECT t.TipoTurno
        FROM Usuario u
        JOIN Turno t ON u.IDTurno = t.ID
        WHERE u.ID=?
        """
        try:
            result = self._execute_query(query, (user_id,))
            return result[0] if result else 0.0
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener el turno del usuario con ID {user_id}: {e}")

    def get_saldo_usuario(self, user_id: int) -> float:
        """
        Obtiene el saldo de un usuario según su ID desde la tabla Tarjeta.
        """
        query = "SELECT Saldo FROM Tarjeta WHERE IDUsuario = ?"
        try:
            self.cursor.execute(query, (user_id,))
            row = self.cursor.fetchone()
            return row[0] if row else 0.0
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener el saldo del usuario con ID {user_id}: {e}")

    def get_type_card(self, user_id: int) -> str:
        """
        Obtiene el tipo de tarjeta de un usuario según su ID desde la tabla Tarjeta y TipoTarjeta.
        """
        query = """
        SELECT tt.Tipo
        FROM Tarjeta t
        JOIN TipoTarjeta tt ON t.IDTipoTarjeta = tt.ID
        WHERE t.IDUsuario = ?
        """
        try:
            self.cursor.execute(query, (user_id,))
            row = self.cursor.fetchone()
            return row[0] if row else ""
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener el tipo de tarjeta del usuario con ID {user_id}: {e}")

    def get_ruta_parada(self, id_ruta: int, id_parada: int):
        """
        Obtiene la relación Ruta-Parada específica por clave compuesta.
        """
        query = "SELECT * FROM RutaParada WHERE IDRuta = ? AND IDParada = ?"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (id_ruta, id_parada))
                row = cursor.fetchone()
                if row is None:
                    return None
                columns = [column[0] for column in cursor.description]
                row_dict = dict(zip(columns, row))
                from backend.app.models.rutaparada import RutaParada
                return RutaParada.model_validate(row_dict)
        except Exception as e:
            logger.error(f"Error en get_ruta_parada: {e}")
            return None

    def delete_ruta_parada(self, id_ruta: int, id_parada: int):
        """
        Elimina la relación Ruta-Parada específica por clave compuesta.
        """
        query = "DELETE FROM RutaParada WHERE IDRuta = ? AND IDParada = ?"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (id_ruta, id_parada))
                self.conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error en delete_ruta_parada: {e}")
            return False

    def update_ruta_parada(self, id_ruta: int, id_parada: int, nuevo_id_ruta: int, nuevo_id_parada: int):
        """
        Actualiza la relación Ruta-Parada específica por clave compuesta.
        """
        query = "UPDATE RutaParada SET IDRuta = ?, IDParada = ? WHERE IDRuta = ? AND IDParada = ?"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (nuevo_id_ruta, nuevo_id_parada, id_ruta, id_parada))
                self.conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error en update_ruta_parada: {e}")
            return False

    def get_ruta_parada_nombres(self) -> list[dict]:
        """
        Devuelve solo el nombre de la ruta y el nombre de la parada para todas las relaciones.
        """
        sql = """
            SELECT r.Nombre AS NombreRuta, p.Nombre AS NombreParada
            FROM RutaParada rp
            JOIN Rutas r ON rp.IDRuta = r.ID
            JOIN Parada p ON rp.IDParada = p.ID
        """
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return [
                {"NombreRuta": row[0], "NombreParada": row[1]}
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error al obtener solo nombres de ruta y parada: {e}")
            raise RuntimeError("Error al obtener solo nombres de ruta y parada")
    def get_all_units_with_schedules(self) -> list[dict]:
        """
        Devuelve todas las unidades de transporte, cada una con su horario (según IDRuta -> Ruta -> IDHorario -> Horario).
        """
        try:
            from backend.app.models.transport import UnidadTransporte
            from backend.app.models.routes import Ruta
            from backend.app.models.schedule import Schedule

            unidades = self.read_all(UnidadTransporte)
            rutas = self.read_all(Ruta)
            horarios = self.read_all(Schedule)

            # Indexar rutas y horarios por ID
            rutas_by_id = {r['ID'] if isinstance(r, dict) else getattr(r, 'ID', None): r for r in rutas}
            horarios_by_id = {h['ID'] if isinstance(h, dict) else getattr(h, 'ID', None): h for h in horarios}

            for unidad in unidades:
                id_ruta = unidad.get('IDRuta') if isinstance(unidad, dict) else getattr(unidad, 'IDRuta', None)
                ruta = rutas_by_id.get(id_ruta)
                id_horario = ruta.get('IDHorario') if ruta else None
                horario = horarios_by_id.get(id_horario)
                unidad['horarios'] = [horario] if horario else []
            return unidades
        except Exception as e:
            logger.error(f"Error al obtener unidades con horarios: {e}")
            raise RuntimeError(f"Error al obtener unidades con horarios: {e}")

    def get_all_units_with_names(self) -> list[dict]:
        """
        Devuelve todas las unidades de transporte, ocultando IDRuta y IDTipo,
        pero trayendo los nombres de la ruta y el tipo de transporte.
        """
        query = """
            SELECT 
                u.ID,
                u.Ubicacion,
                u.Capacidad,
                r.Nombre AS NombreRuta,
                t.TipoTransporte AS NombreTipoTransporte
            FROM UnidadTransporte u
            LEFT JOIN Rutas r ON u.IDRuta = r.ID
            LEFT JOIN TipoTransporte t ON u.IDTipo = t.ID
        """
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            columns = [column[0] for column in self.cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener unidades con nombres: {e}")
            raise RuntimeError(f"Error al obtener unidades con nombres: {e}")

