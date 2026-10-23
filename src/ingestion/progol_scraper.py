import sqlite3 
import requests 
from bs4 import BeautifulSoup 
from config.settings import settings 
 
def guardar_jornada_progol(numero_jornada, lista_partidos): 
    conn = sqlite3.connect(settings.DB_PATH) 
    cursor = conn.cursor() 
 
    for p in lista_partidos: 
        cursor.execute("INSERT OR IGNORE INTO equipos (nombre, liga) VALUES (?, 'Progol')", (p['local'],)) 
        cursor.execute("INSERT OR IGNORE INTO equipos (nombre, liga) VALUES (?, 'Progol')", (p['visitante'],)) 
        cursor.execute("SELECT id FROM equipos WHERE nombre = ?", (p['local'],)) 
        id_local = cursor.fetchone()[0] 
        cursor.execute("SELECT id FROM equipos WHERE nombre = ?", (p['visitante'],)) 
        id_visitante = cursor.fetchone()[0] 
 
        cursor.execute("INSERT INTO partidos (fecha, equipo_local_id, equipo_visitante_id) VALUES (?, ?, ?)", 
                       ('2026-10-24', id_local, id_visitante)) 
        partido_id = cursor.lastrowid 
 
        cursor.execute("INSERT INTO metricas_avanzadas (partido_id, local_xg, visitante_xg, local_xga, visitante_xga) VALUES (?, ?, ?, ?, ?)", 
                       (partido_id, p['local_xg'], p['visitante_xg'], 1.0, 1.0)) 
 
        cursor.execute("INSERT INTO progol_jornadas (numero_jornada, partido_id, pct_local_publico, pct_empate_publico, pct_visitante_publico) VALUES (?, ?, ?, ?, ?)", 
                       (numero_jornada, partido_id, p['pct_l'], p['pct_e'], p['pct_v'])) 
 
    conn.commit() 
    conn.close() 
    print(f"Jornada {numero_jornada} de Progol guardada exitosamente en la base de datos.") 
 
if __name__ == "__main__": 
    jornada_demo = [ 
        {'local': 'America', 'visitante': 'Chivas', 'local_xg': 1.85, 'visitante_xg': 1.10, 'pct_l': 65.0, 'pct_e': 20.0, 'pct_v': 15.0}, 
        {'local': 'Cruz Azul', 'visitante': 'Pumas', 'local_xg': 1.40, 'visitante_xg': 1.25, 'pct_l': 45.0, 'pct_e': 30.0, 'pct_v': 25.0} 
    ] 
    guardar_jornada_progol(2250, jornada_demo)
