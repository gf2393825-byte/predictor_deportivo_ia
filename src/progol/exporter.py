import csv
from pathlib import Path

def exportar_boletas(jornada, resultados, partidos_info=None):
    """
    Exporta las boletas optimizadas a formato CSV y TXT.
    """
    output_dir = Path("exports")
    output_dir.mkdir(exist_ok=True)
    
    csv_file = output_dir / f"progol_jornada_{jornada}_optimizada.csv"
    txt_file = output_dir / f"progol_jornada_{jornada}_boletas.txt"
    
    # 1. Exportación a CSV
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f_csv:
        writer = csv.writer(f_csv)
        header = ["Boleta_ID", "EV_Acumulado"] + [f"Casilla_{i}" for i in range(1, 15)]
        writer.writerow(header)
        
        for i, (boleta, ev) in enumerate(resultados, 1):
            row = [f"Boleta_{i:02d}", f"{ev:.2f}"] + list(boleta)
            writer.writerow(row)
            
    # 2. Exportación a TXT (Formato de Lectura / Impresión)
    with open(txt_file, mode="w", encoding="utf-8") as f_txt:
        f_txt.write("============================================================\n")
        f_txt.write(f"    PREDICTOR DEPORTIVO IA - BOLETAS PROGOL (JORNADA {jornada})\n")
        f_txt.write("============================================================\n\n")
        
        for i, (boleta, ev) in enumerate(resultados, 1):
            boleta_str = "  ".join(boleta)
            f_txt.write(f"BOLETA #{i:02d} | EV ACUMULADO: {ev:.2f}\n")
            f_txt.write(f"Jugada: [ {boleta_str} ]\n")
            f_txt.write("-" * 60 + "\n")
            
    print(f"[+] Archivos generados exitosamente en /exports:")
    print(f"    - CSV: {csv_file}")
    print(f"    - TXT: {txt_file}")

if __name__ == "__main__":
    from src.progol.combinatorio import generar_combinaciones_reducidas
    boletas = generar_combinaciones_reducidas(2252, max_boletas=5)
    exportar_boletas(2252, boletas)