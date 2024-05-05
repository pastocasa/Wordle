from typing import List
import mysql.connector as bd
import constantes
from constantes import BD_DATABASE, BD_HOSTNAME, BD_PASSWORD, BD_USERNAME
import random

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

def jugador_existe(conn:bd.MySQLConnection, nombre):
    if consulta_generica(conn, f'SELECT count(id) FROM wordle.jugadores WHERE nombre = "{nombre}"') == 1:
        return True
    return False

def cargar_jugador(conn:bd.MySQLConnection, nombre):
    if jugador_existe(conn, nombre) == True:
        raise ValueError(f"El nombre {nombre} ya esta en uso")
    modificacion_generica(conn, f'INSERT INTO wordle.jugadores(nombre) VALUES("{nombre}")')
    return consulta_generica(conn, "SELECT * FROM wordle.jugadores ORDER BY id desc LIMIT 1")

def buscar_jugador(conn:bd.MySQLConnection, nombre):
    if jugador_existe(conn, nombre) == False:
        raise ValueError(f"{nombre} no existe en la base de datos")
    id = consulta_generica(conn, f'SELECT id from wordle.jugadores WHERE nombre = "{nombre}"')
    return "a"

def cargar_resultado(conn:bd.MySQLConnection, id_palabra, id_jugador, intentos):
    if intentos < 0 or intentos > 6:
        raise ValueError("Cantidad de intentos inválida")
    modificacion_generica(conn, f'INSERT INTO wordle.jugadas(palabra, jugador, intentos) VALUES({id_palabra}, {id_jugador}, {intentos})')
    return consulta_generica(conn, f'SELECT * from wordle.jugadas WHERE palabra = {id_palabra} and jugador = {id_jugador}')

#a ver si ahora el github hace algo aaaaaaaaaaaaaaa

def obtener_ids_jugadas(conn:bd.MySQLConnection, id_jugador):
    ids_jugadas = consulta_generica(conn, f'SELECT palabra FROM wordle.jugadas WHERE jugador = {id_jugador}')
    if len(ids_jugadas) < 1:
        raise ValueError("El jugador ingresado todavía no jugó")
    return ids_jugadas

def obtener_palabra_al_azar(conn:bd.MySQLConnection):
    ultimo_id = consulta_generica(conn, 'SELECT id FROM wordle.palabras ORDER BY id desc limit 1')
    id_palabra = 3 #random.randint(1, ultimo_id)
    palabras_jugadas = obtener_ids_jugadas(conn, 1)
    for i in palabras_jugadas[0]:
        while id_palabra == i:
            id_palabra = random.randint(1, ultimo_id[0][0])
    return consulta_generica(conn, f'SELECT palabra FROM wordle.palabras WHERE id = {id_palabra}')
#falta testear esta función