import sqlite3
from datetime import datetime

NOMBRE_DB = "home_guardian.db"

def conectar():
    return sqlite3.connect(NOMBRE_DB)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dispositivos (
            mac TEXT PRIMARY KEY,
            ip TEXT,
            primera_vez_visto TEXT,
            ultima_vez_visto TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escaneos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mac TEXT,
            ip TEXT,
            fecha_hora TEXT
        )
    """)

    conn.commit()
    conn.close()

def registrar_dispositivo(mac, ip):
    """Devuelve True si es un dispositivo nuevo (nunca visto antes), False si ya existía."""
    conn = conectar()
    cursor = conn.cursor()
    ahora = datetime.now().isoformat(timespec="seconds")

    cursor.execute("SELECT mac FROM dispositivos WHERE mac = ?", (mac,))
    existe = cursor.fetchone()

    if existe:
        cursor.execute(
            "UPDATE dispositivos SET ip = ?, ultima_vez_visto = ? WHERE mac = ?",
            (ip, ahora, mac)
        )
        es_nuevo = False
    else:
        cursor.execute(
            "INSERT INTO dispositivos (mac, ip, primera_vez_visto, ultima_vez_visto) VALUES (?, ?, ?, ?)",
            (mac, ip, ahora, ahora)
        )
        es_nuevo = True

    cursor.execute(
        "INSERT INTO escaneos (mac, ip, fecha_hora) VALUES (?, ?, ?)",
        (mac, ip, ahora)
    )

    conn.commit()
    conn.close()
    return es_nuevo

def obtener_todos_los_dispositivos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT mac, ip, primera_vez_visto, ultima_vez_visto FROM dispositivos")
    filas = cursor.fetchall()
    conn.close()
    return [
        {"mac": f[0], "ip": f[1], "primera_vez_visto": f[2], "ultima_vez_visto": f[3]}
        for f in filas
    ]