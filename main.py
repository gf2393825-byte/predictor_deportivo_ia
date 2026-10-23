import sys
from src.progol.combinatorio import generar_combinaciones_reducidas
from src.progol.exporter import exportar_boletas

def ejecutar_pipeline_progol(jornada=2252, num_boletas=5):
    print("=" * 60)
    print("   PREDICTOR DEPORTIVO IA - SISTEMA DE OPTIMIZACION PROGOL")
    print("=" * 60)
    print(f"[*] Procesando datos de la Jornada {jornada} desde SQLite...")
    
    resultados = generar_combinaciones_reducidas(jornada, max_boletas=num_boletas)
    
    if not resultados:
        print(f"[!] No se generaron combinaciones para la jornada {jornada}.")
        return

    print(f"\n[+] TOP {len(resultados)} BOLETAS SUGERIDAS (+EV AGREGADO):")
    print("-" * 60)
    for i, (boleta, ev) in enumerate(resultados, 1):
        boleta_formatted = "  ".join(boleta)
        print(f" Boleta {i:02d} -> [ {boleta_formatted} ]  |  EV Acumulado: {ev:.2f}")
    print("-" * 60)
    
    # Exportar resultados automáticamente
    exportar_boletas(jornada, resultados)

if __name__ == "__main__":
    jornada_input = 2252
    if len(sys.argv) > 1:
        try:
            jornada_input = int(sys.argv[1])
        except ValueError:
            pass
    ejecutar_pipeline_progol(jornada_input)