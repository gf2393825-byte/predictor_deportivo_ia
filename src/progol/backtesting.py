import sqlite3
from config.settings import settings
from src.progol.combinatorio import generar_combinaciones_reducidas

def registrar_resultados_reales(numero_jornada, quiniela_ganadora):
    """
    Registra en la base de datos la secuencia ganadora de 14 resultados reales
    para una jornada (ejemplo: ['1', 'X', '2', '1', '1', 'X', ...])
    """
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    
    # Crear tabla de resultados oficiales si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados_oficiales (
            numero_jornada INTEGER PRIMARY KEY,
            resultado_string TEXT
        )
    """)
    
    resultado_str = "".join(quiniela_ganadora)
    cursor.execute(
        "INSERT OR REPLACE INTO resultados_oficiales (numero_jornada, resultado_string) VALUES (?, ?)",
        (numero_jornada, resultado_str)
    )
    conn.commit()
    conn.close()
    print(f"[+] Resultados oficiales de la Jornada {numero_jornada} registrados en DB.")

def evaluar_rendimiento_jornada(numero_jornada, top_boletas=5):
    conn = sqlite3.connect(settings.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT resultado_string FROM resultados_oficiales WHERE numero_jornada = ?", (numero_jornada,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        print(f"[!] No hay resultados reales registrados para la Jornada {numero_jornada}.")
        return
        
    resultado_real = list(row[0])
    boletas_optimizadas = generar_combinaciones_reducidas(numero_jornada, max_boletas=top_boletas)
    
    print("\n" + "=" * 65)
    print(f" REPORTES DE BACKTESTING - JORNADA {numero_jornada}")
    print("=" * 65)
    print(f"Resultado Ganador Oficial: [ {' '.join(resultado_real)} ]\n")
    
    for i, (boleta, ev) in enumerate(boletas_optimizadas, 1):
        aciertos = sum(1 for b, r in zip(boleta, resultado_real) if b == r)
        print(f" Boleta #{i:02d} | EV: {ev:.2f} | Aciertos: {aciertos}/14")
    print("=" * 65)

if __name__ == "__main__":
    # Prueba de simulación con un resultado real de prueba para la Jornada 2253
    resultado_real_demo = ["1", "1", "1", "1", "X", "1", "1", "1", "X", "1", "1", "X", "1", "1"]
    registrar_resultados_reales(2253, resultado_real_demo)
    evaluar_rendimiento_jornada(2253)