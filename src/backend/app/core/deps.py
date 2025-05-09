import os
import sqlite3
from typing import Any

# Definir la ruta a la base de datos
PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'src', 'backend', 'app', 'data')
DB_FILE = os.path.join(DIR_DATA, 'data.db')
#Pasajero
def obtener_ruta_con_interconexion(ubicacion_llegada, ubicacion_final):
    answer = ""  # Initialize answer
    try:
        # Conectarse a la base de datos
        conexion = sqlite3.connect('data.db')
        cursor = conexion.cursor()

        # Obtener rutas desde la ubicación de llegada
        query_llegada = '''
        SELECT r.id, r.name, p.id, p.ubication
        FROM ruta r
        JOIN rutaparada rp ON r.id = rp.idruta
        JOIN parada p ON rp.idparada = p.id
        WHERE p.ubication = ?;
        '''
        cursor.execute(query_llegada, (ubicacion_llegada,))
        rutas_llegada = cursor.fetchall()

        for ruta_id, ruta_name, parada_id, parada_ubicacion in rutas_llegada:
            # Obtener rutas que lleguen a la ubicación final
            query_final = '''
            SELECT r.id, r.name, p.id, p.ubication
            FROM ruta r
            JOIN rutaparada rp ON r.id = rp.idruta
            JOIN parada p ON rp.idparada = p.id
            WHERE p.ubication = ?;
            '''
            cursor.execute(query_final, (ubicacion_final,))
            rutas_final = cursor.fetchall()

            for ruta_final_id, ruta_final_name, parada_final_id, parada_final_ubicacion in rutas_final:
                # Verificar interconexión entre rutas
                query_interconexion = '''
                SELECT p.id, p.ubication
                FROM parada p
                JOIN rutaparada rp1 ON p.id = rp1.idparada
                JOIN rutaparada rp2 ON p.id = rp2.idparada
                WHERE rp1.idruta = ? AND rp2.idruta = ?;
                '''
                cursor.execute(query_interconexion, (ruta_id, ruta_final_id))
                interconexiones = cursor.fetchall()
                for inter_parada_id, inter_ubicacion in interconexiones:
                    answer += f"\n Ruta de inicio: {ruta_name}, Interconexión: {inter_ubicacion}, Ruta final: {ruta_final_name}\n"

        # Cerrar la conexión
        cursor.close()
        conexion.close()
    
    except sqlite3.Error as error:
        print(f'Error al ejecutar el query: {error}')
    
    return answer

#Pasajero
def ultimo_uso_tarjeta(id_tarjeta: int) -> str:
    """Get the last usage date of a card."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    sql = "SELECT fecha_uso FROM tarjeta WHERE id = ?"
    cursor.execute(sql, (id_tarjeta,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
def total_unidades() -> int:
    """Get the total number of units."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM unidadtransporte"
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0
def total_pasajeros() -> int:
    """Get the total number of passengers."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM Usuario WHERE IDRolUsuario = 1"
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0
def total_operario()-> int:
    """Get the total number of operators."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM usuario WHERE IDRolUsuario = 2"
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0
def total_supervisor()-> int:
    """Get the total number of supervisors."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM usuario WHERE IDRolUsuario = 3"
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0
def get_type_card(ID_usuario: int) -> list:
    """Get the type of card for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    sql = "SELECT tipotarjeta.type FROM tipotarjeta INNER JOIN tarjeta ON tipotarjeta.id = tarjeta.idtype WHERE tarjeta.iduser = ?;"
    cursor.execute(sql, (ID_usuario,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
def total_mantenimiento() -> int:
    """Get the total number of maintenance records."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM mantenimiento"
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0
def proximos_mantenimientos() -> list:
    """Get the next maintenance records."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    sql = "SELECT * FROM mantenimiento WHERE fecha > DATE('now')"
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows if rows else 0