from typing import List
import mysql.connector as bd
import constantes
from constantes import BD_DATABASE, BD_HOSTNAME, BD_PASSWORD, BD_USERNAME 

def abrir_conexion() -> bd.pooling.PooledMySQLConnection | bd.MySQLConnection:
    return bd.connect(host=BD_HOSTNAME,
                    user=BD_USERNAME,
                    password=BD_PASSWORD,
                    database=BD_DATABASE)

def consulta_generica(conn : bd.MySQLConnection, consulta : str) -> List[bd.connection.RowType]:
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta)
    return cursor.fetchall()

def modificacion_generica(conn:bd.MySQLConnection, consulta):
    cursor = conn.cursor(buffered=True)
    cursor.execute(consulta)
    conn.commit()
    return cursor.rowcount

def cargar_jugador(conn:bd.MySQLConnection, nombre):
    modificacion_generica(conn, f'INSERT INTO wordle.jugadores(nombre) VALUES("{nombre}")')
    return consulta_generica(conn, "SELECT * FROM ventas.ordenes ORDER BY id desc LIMIT 1")