import sqlite3
import pandas as pd
from config.settings import settings

def cargar_datos_prueba():
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()

    # Insertar equipos de muestra
    equipos = [("America", "Liga MX"), ("Chivas", "Liga MX"), ("Cruz Azul", "Liga MX"), ("Pumas", "Liga MX")]
    for eq, liga in equipos:
        cursor.execute("INSERT OR IGNORE INTO equipos (nombre, liga) VALUES (?, ?)", (eq, liga))

    conn.commit()
    conn.close()
    print("Datos base cargados correctamente.")

if __name__ == "__main__":
    cargar_datos_prueba()
