from pathlib import Path 
import itertools 
from config.settings import settings 
from src.models.dixon_coles import calcular_probabilidades_partido 
from src.progol.optimizer import evaluar_valor_partido 
 
def cargar_partidos_jornada(numero_jornada): 
    conn = sqlite3.connect(settings.DB_PATH) 
    cursor = conn.cursor() 
    query = ''' 
    SELECT p.id, e_loc.nombre as local, e_vis.nombre as visitante, m.local_xg, m.visitante_xg, pj.pct_local_publico, pj.pct_empate_publico, pj.pct_visitante_publico 
    FROM progol_jornadas pj 
    JOIN partidos p ON pj.partido_id = p.id 
    JOIN equipos e_loc ON p.equipo_local_id = e_loc.id 
    JOIN equipos e_vis ON p.equipo_visitante_id = e_vis.id 
    JOIN metricas_avanzadas m ON p.id = m.partido_id 
    WHERE pj.numero_jornada = ? 
    ''' 
    cursor.execute(query, (numero_jornada,)) 
    filas = cursor.fetchall() 
    conn.close() 
    return filas 
def generar_combinaciones_reducidas(jornada, max_boletas=10): 
    partidos = cargar_partidos_jornada(jornada) 
    if not partidos: 
        print('No hay datos para esta jornada.') 
        return 
    posibilidades_por_partido = [] 
    for p in partidos: 
        p_id, loc, vis, xg_l, xg_v, pct_l, pct_e, pct_v = p 
        probs = calcular_probabilidades_partido(xg_l, xg_v) 
        ev_l = evaluar_valor_partido(probs['prob_local'], pct_l) 
        ev_e = evaluar_valor_partido(probs['prob_empate'], pct_e) 
        ev_v = evaluar_valor_partido(probs['prob_visitante'], pct_v) 
        posibilidades_por_partido.append([('1', ev_l), ('X', ev_e), ('2', ev_v)]) 
    combinaciones_validas = [] 
    for quiniela in itertools.product(*posibilidades_por_partido): 
        selecciones = [s[0] for s in quiniela] 
        ev_total = sum(s[1] for s in quiniela) 
        empates = selecciones.count('X') 
        if 0 <= empates <= 6: 
            combinaciones_validas.append((tuple(selecciones), ev_total)) 
    combinaciones_ordenadas = sorted(combinaciones_validas, key=lambda x: x[1], reverse=True) 
    return combinaciones_ordenadas[:max_boletas] 
 
if __name__ == '__main__': 
    resultados = generar_combinaciones_reducidas(2250, max_boletas=5) 
    print('\n=== TOP 5 BOLETAS OPTIMIZADAS (+EV) - JORNADA 2250 ===') 
    for i, (boleta, ev) in enumerate(resultados, 1): 
        print(f'Boleta {i}: {" ".join(boleta)} | Indice EV Acumulado: {ev:.2f}') 
