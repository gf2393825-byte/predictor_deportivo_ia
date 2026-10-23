import numpy as np
from src.models.dixon_coles import calcular_probabilidades_partido

def evaluar_valor_partido(prob_modelo, pct_publico):
    """Calcula el indice de valor respecto a la estimacion del publico."""
    pct_pub_norm = max(pct_publico / 100.0, 0.01)
    return round(prob_modelo / pct_pub_norm, 2)

def filtrar_quiniela_valida(combinacion):
    """
    Filtros de estructura para descartar patrones inverosimiles.
    combinacion: lista de 14 resultados ['1', 'X', '2', ...]
    """
    empates = combinacion.count('X')
    visitantes = combinacion.count('2')
    
    # Filtro 1: Cantidad de empates aceptables (entre 2 y 6)
    if not (2 <= empates <= 6):
        return False
        
    # Filtro 2: Cantidad de victorias visitantes (entre 3 y 7)
    if not (3 <= visitantes <= 7):
        return False
        
    return True

def simular_jornada_progol(partidos_xg, estimados_publico):
    """
    Modela los 14 partidos de Progol e identifica los de mayor valor.
    """
    jornada_resultados = []
    for idx, (xg_l, xg_v) in enumerate(partidos_xg):
        probs = calcular_probabilidades_partido(xg_l, xg_v)
        pub = estimados_publico[idx]
        
        ev_l = evaluar_valor_partido(probs["prob_local"], pub["L"])
        ev_e = evaluar_valor_partido(probs["prob_empate"], pub["E"])
        ev_v = evaluar_valor_partido(probs["prob_visitante"], pub["V"])
        
        jornada_resultados.append({
            "partido": idx + 1,
            "probs": probs,
            "ev": {"L": ev_l, "E": ev_e, "V": ev_v}
        })
    return jornada_resultados

if __name__ == "__main__":
    # Ejemplo con 1 partido simulado
    partidos_demo = [(1.85, 1.10)]
    publico_demo = [{"L": 65.0, "E": 20.0, "V": 15.0}]
    
    res = simular_jornada_progol(partidos_demo, publico_demo)[0]
    print("--- Analisis de Valor para Progol ---")
    print(f"Partido 1:")
    print(f"  Probabilidades Modelo - {res['probs']['prob_local']*100:.1f}%, E: {res['probs']['prob_empate']*100:.1f}%, V: {res['probs']['prob_visitante']*100:.1f}%")
    print(f"  Relacion de Valor (+EV) - {res['ev']['L']}, Empate: {res['ev']['E']}, Visitante: {res['ev']['V']}")
