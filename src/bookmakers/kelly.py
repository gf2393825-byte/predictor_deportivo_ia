def remover_vig(cuota_local, cuota_empate, cuota_visitante):
    """Calcula la probabilidad real del mercado removiendo el margen comercial."""
    prob_impl_l = 1.0 / cuota_local
    prob_impl_e = 1.0 / cuota_empate
    prob_impl_v = 1.0 / cuota_visitante
    overround = prob_impl_l + prob_impl_e + prob_impl_v
    return {
        "p_real_l": round(prob_impl_l / overround, 4),
        "p_real_e": round(prob_impl_e / overround, 4),
        "p_real_v": round(prob_impl_v / overround, 4),
        "overround_pct": round((overround - 1.0) * 100, 2)
    }

def evaluar_apuesta_kelly(prob_modelo, cuota_decimal, fraccion_kelly=0.25):
    """
    Calcula el Valor Esperado (+EV) y el tamaño del Stake segun Criterio de Kelly.
    """
    ev = (prob_modelo * cuota_decimal) - 1.0
    if ev <= 0:
        return {"apostar": False, "ev": round(ev, 4), "stake_pct": 0.0}
    
    b = cuota_decimal - 1.0
    p = prob_modelo
    q = 1.0 - p
    f_kelly = (p * b - q) / b
    stake_recomendado = round(max(f_kelly * fraccion_kelly, 0.0) * 100, 2)
    
    return {"apostar": True, "ev": round(ev, 4), "stake_pct": stake_recomendado}

if __name__ == "__main__":
    # Ejemplo: Probabilidad Modelo Local = 54.2%, Cuota ofrecida por la casa = 2.10
    c_l, c_e, c_v = 2.10, 3.40, 3.60
    vig_info = remover_vig(c_l, c_e, c_v)
    res_kelly = evaluar_apuesta_kelly(prob_modelo=0.542, cuota_decimal=c_l)
    
    print("--- Analisis para Casas de Apuestas ---")
    print(f"Margen de la Casa (Vig): {vig_info['overround_pct']}%")
    print(f"Valor Esperado (+EV): {res_kelly['ev']}")
    print(f"Apostar?: {'SI' if res_kelly['apostar'] else 'NO'}")
    print(f"Stake Recomendado (Kelly 0.25): {res_kelly['stake_pct']}% del Bankroll")
