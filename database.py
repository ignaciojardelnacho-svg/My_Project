import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="torneo_futbol"
    )

def inicializar_bd():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conexion.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS torneo_futbol")
    cursor.execute("USE torneo_futbol")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            grupo VARCHAR(10)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partidos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            equipo_local_id INT,
            equipo_visitante_id INT,
            goles_local INT DEFAULT 0,
            goles_visitante INT DEFAULT 0,
            jugado BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (equipo_local_id) REFERENCES equipos(id),
            FOREIGN KEY (equipo_visitante_id) REFERENCES equipos(id)
        )
    """)

    conexion.commit()
    cursor.close()
    conexion.close()

def guardar_equipo(nombre, grupo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO equipos (nombre, grupo) VALUES (%s, %s)", (nombre, grupo))
    conexion.commit()
    id_insertado = cursor.lastrowid
    cursor.close()
    conexion.close()
    return id_insertado

def guardar_partido(local_id, visitante_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO partidos (equipo_local_id, equipo_visitante_id) VALUES (%s, %s)",
        (local_id, visitante_id)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

def registrar_resultado_bd(partido_id, goles_local, goles_visitante):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE partidos SET goles_local = %s, goles_visitante = %s, jugado = TRUE WHERE id = %s",
        (goles_local, goles_visitante, partido_id)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_equipos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM equipos")
    equipos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return equipos

def obtener_partidos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, e1.nombre AS local, e2.nombre AS visitante, 
               p.goles_local, p.goles_visitante, p.jugado
        FROM partidos p
        JOIN equipos e1 ON p.equipo_local_id = e1.id
        JOIN equipos e2 ON p.equipo_visitante_id = e2.id
    """)
    partidos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return partidos
