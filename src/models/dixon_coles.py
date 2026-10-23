import math

def poisson_pmf(k, mu):
    """Calcula la probabilidad puntual de Poisson."""
    return (math.pow(mu, k) * math.exp(-mu)) / math.factorial(k)

def ajuste_tau(x, y, lambda_l, mu_v, tau=0.10):
    """
    Aplica la corrección de dependencia Dixon-Coles para marcadores bajos:
    (0-0), (1-0), (0-1) y (1-1).
    """
    if x == 0 and y == 0:
        return 1.0 - (lambda_l * mu_v * tau)
    elif x == 1 and y == 0:
        return 1.0 + (lambda_l * tau)
    elif x == 0 and y == 1:
        return 1.0 + (mu_v * tau)
    elif x == 1 and y == 1:
        return 1.0 - tau
    else:
        return 1.0

def calcular_probabilidades_partido(local_xg, visitante_xg, max_goles=7, tau=0.10):
    """
    Genera la matriz de probabilidades exactas aplicando Dixon-Coles calibrado.
    """
    prob_local = 0.0
    prob_empate = 0.0
    prob_visitante = 0.0

    for x in range(max_goles + 1):
        for y in range(max_goles + 1):
            p_x = poisson_pmf(x, local_xg)
            p_y = poisson_pmf(y, visitante_xg)
            
            # Aplicar factor de correlación tau
            factor = ajuste_tau(x, y, local_xg, visitante_xg, tau)
            prob_exacta = max(0.0, p_x * p_y * factor)
            
            if x > y:
                prob_local += prob_exacta
            elif x == y:
                prob_empate += prob_exacta
            else:
                prob_visitante += prob_exacta

    # Normalización para asegurar suma igual a 1.0
    total = prob_local + prob_empate + prob_visitante
    return {
        "prob_local": prob_local / total,
        "prob_empate": prob_empate / total,
        "prob_visitante": prob_visitante / total
    }

if __name__ == "__main__":
    # Prueba de calibración sobre un partido típico
    res = calcular_probabilidades_partido(1.4, 1.1, tau=0.10)
    print(f"Probabilidades Calibradas -> Local: {res['prob_local']:.1%}, Empate: {res['prob_empate']:.1%}, Visitante: {res['prob_visitante']:.1%}")