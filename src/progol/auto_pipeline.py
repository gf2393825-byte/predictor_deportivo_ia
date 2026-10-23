import sys
import datetime
from src.progol.progol_scraper import descargar_y_cargar_jornada
from src.progol.xg_fetcher import actualizar_metricas_jornada_real
from src.progol.combinatorio import generar_combinaciones_reducidas
from src.progol.exporter import exportar_boletas

def ejecutar_autoproceso(jornada_numero, top_boletas=5):
    hora_inicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 65)
    print(f" PREDICTOR DEPORTIVO IA - AUTOMATIZACION DE JORNDAS PROGOL")
    print(f" Ejecutado: {hora_inicio}")
    print("=" * 65)
    
    # 1. Scraping / Ingesta de datos de la jornada
    print(f"\n[1/4] Descargando e ingresando casillas de la Jornada {jornada_numero}...")
    descargar_y_cargar_jornada(jornada_numero)
    
    # 2. Inyección de métricas avanzadas (xG / xGA reales)
    print(f"\n[2/4] Sincronizando xG y xGA reales desde fuentes internacionales...")
    actualizar_metricas_jornada_real(jornada_numero)
    
    # 3. Generación de combinaciones con filtros +EV
    print(f"\n[3/4] Calculando Dixon-Coles y filtrando combinaciones (+EV)...")
    boletas = generar_combinaciones_reducidas(jornada_numero, max_boletas=top_boletas)
    
    if not boletas:
        print(f"[!] No se pudieron generar boletas para la Jornada {jornada_numero}.")
        return
        
    # 4. Exportación de archivos CSV y TXT
    print(f"\n[4/4] Exportando reportes a la carpeta /exports...")
    exportar_boletas(jornada_numero, boletas)
    
    print("\n" + "=" * 65)
    print(f" [✓] Proceso completado exitosamente para la Jornada {jornada_numero}")
    print("=" * 65)

if __name__ == "__main__":
    jornada_defecto = 2254
    if len(sys.argv) > 1:
        try:
            jornada_defecto = int(sys.argv[1])
        except ValueError:
            pass
    ejecutar_autoproceso(jornada_defecto)