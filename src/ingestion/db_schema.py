import sqlite3
from config.settings import settings

def init_db():
    settings.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()

    # Tabla de Equipos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS equipos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        liga TEXT NOT NULL
    )''')

    # Tabla de Partidos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS partidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        equipo_local_id INTEGER NOT NULL,
        equipo_visitante_id INTEGER NOT NULL,
        goles_local INTEGER,
        goles_visitante INTEGER,
        FOREIGN KEY(equipo_local_id) REFERENCES equipos(id),
        FOREIGN KEY(equipo_visitante_id) REFERENCES equipos(id)
    )''')

    # Tabla de Metricas Avanzadas (xG)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS metricas_avanzadas (
        partido_id INTEGER PRIMARY KEY,
        local_xg REAL NOT NULL,
        visitante_xg REAL NOT NULL,
        local_xga REAL NOT NULL,
        visitante_xga REAL NOT NULL,
        FOREIGN KEY(partido_id) REFERENCES partidos(id)
    )''')

    # Tabla de Cuotas de Mercado
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cuotas_mercado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partido_id INTEGER NOT NULL,
        cuota_local REAL NOT NULL,
        cuota_empate REAL NOT NULL,
        cuota_visitante REAL NOT NULL,
        es_clv INTEGER DEFAULT 0,
        FOREIGN KEY(partido_id) REFERENCES partidos(id)
    )''')

    # Tabla de Progol (Estimaciones Publicas)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progol_jornadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_jornada INTEGER NOT NULL,
        partido_id INTEGER NOT NULL,
        pct_local_publico REAL NOT NULL,
        pct_empate_publico REAL NOT NULL,
        pct_visitante_publico REAL NOT NULL,
        FOREIGN KEY(partido_id) REFERENCES partidos(id)
    )''')

    conn.commit()
    conn.close()
    print("Base de datos inicializada exitosamente.")

if __name__ == "__main__":
    init_db()
