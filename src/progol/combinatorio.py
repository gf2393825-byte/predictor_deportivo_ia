import sqlite3
import itertools
from config.settings import settings
from src.models.dixon_coles import calcular_probabilidades_partido
from src.progol.optimizer import evaluar_valor_partido

def cargar_partidos_jornada(numero_jornada):
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    query = """
    SELECT 
        p.id,
        e_loc.nombre as local,
        e_vis.nombre as visitante,
        m.local_xg,
        m.visitante_xg,
        pj.pct_local_publico,
        pj.pct_empate_publico,
        pj.pct_visitante_publico
    FROM progol_jornadas pj
    JOIN partidos p ON pj.partido_id = p.id
    JOIN equipos e_loc ON p.equipo_local_id = e_loc.id
    JOIN equipos e_vis ON p.equipo_visitante_id = e_vis.id
    JOIN metricas_avanzadas m ON p.id = m.partido_id
    WHERE pj.numero_jornada = ?
    """
    cursor.execute(query, (numero_jornada,))
    filas = cursor.fetchall()
    conn.close()
    return filas

def es_combinacion_valida(selecciones):
    """
    Filtros estructurales para quinielas de 14 partidos:
    - Empates (X): entre 3 y 6.
    - Visitantes (2): máximo 6.
    - Rachas consecutivas: máximo 4 repeticiones del mismo signo seguidas.
    """
    empates = selecciones.count("X")
    visitantes = selecciones.count("2")
    
    if not (3 <= empates <= 6):
        return False
    if visitantes > 6:
        return False
        
    # Verificar rachas (no más de 4 seguidos del mismo signo)
    max_racha = 1
    racha_actual = 1
    for i in range(1, len(selecciones)):
        if selecciones[i] == selecciones[i-1]:
            racha_actual += 1
            if racha_actual > max_racha:
                max_racha = racha_actual
        else:
            racha_actual = 1
            
    if max_racha > 4:
        return False
        
    return True

def generar_combinaciones_reducidas(jornada, max_boletas=10):
    partidos = cargar_partidos_jornada(jornada)
    if not partidos:
        print(f"[!] No hay datos para la jornada {jornada}.")
        return []
        
    posibilidades_por_partido = []
    for p in partidos:
        p_id, loc, vis, xg_l, xg_v, pct_l, pct_e, pct_v = p
        probs = calcular_probabilidades_partido(xg_l, xg_v)
        ev_l = evaluar_valor_partido(probs["prob_local"], pct_l)
        ev_e = evaluar_valor_partido(probs["prob_empate"], pct_e)
        ev_v = evaluar_valor_partido(probs["prob_visitante"], pct_v)
        posibilidades_por_partido.append([("1", ev_l), ("X", ev_e), ("2", ev_v)])
        
    combinaciones_validas = []
    for quiniela in itertools.product(*posibilidades_por_partido):
        selecciones = [s[0] for s in quiniela]
        if es_combinacion_valida(selecciones):
            ev_total = sum(s[1] for s in quiniela)
            combinaciones_validas.append((tuple(selecciones), ev_total))
            
    combinaciones_ordenadas = sorted(combinaciones_validas, key=lambda x: x[1], reverse=True)
    return combinaciones_ordenadas[:max_boletas]

if __name__ == "__main__":
    resultados = generar_combinaciones_reducidas(2252, max_boletas=5)
    print("\n=== TOP 5 BOLETAS OPTIMIZADAS CON FILTROS AVANZADOS (JORNADA 2252) ===")
    for i, (boleta, ev) in enumerate(resultados, 1):
        boleta_str = " ".join(boleta)
        print(f"Boleta {i:02d}: [ {boleta_str} ] -- EV Acumulado: {ev:.2f}")