import wfdb
import os
import csv
from tqdm import tqdm

def procesar_anotaciones(ruta_base, archivo_pu):
    try:
        # Leer las anotaciones usando wfdb.rdann
        anotaciones = wfdb.rdann(ruta_base, 'pu')
        
        # Crear nombre del archivo CSV
        nombre_base = os.path.basename(ruta_base)
        csv_filename = os.path.join('annotations', f'{nombre_base}.csv')
        
        # Guardar las anotaciones N, t y sus paréntesis en el CSV
        with open(csv_filename, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'Sample #', 'Type'])  # encabezado

            i = 0
            while i < len(anotaciones.sample) - 2:
                simbolo1 = anotaciones.symbol[i]
                simbolo2 = anotaciones.symbol[i + 1]
                simbolo3 = anotaciones.symbol[i + 2]
                
                # Patrón ( N )
                if simbolo1 == '(' and simbolo2 == 'N' and simbolo3 == ')':
                    # Guardar el grupo completo
                    for j in range(3):
                        idx = i + j
                        tiempo = anotaciones.sample[idx] / anotaciones.fs
                        time_str = f"{tiempo:.3f}"
                        sample = anotaciones.sample[idx]
                        tipo = anotaciones.symbol[idx]
                        writer.writerow([time_str, sample, tipo])
                    i += 3
                
                # Patrón ( N N )
                elif i < len(anotaciones.sample) - 3 and simbolo1 == '(' and simbolo2 == 'N' and simbolo3 == 'N' and anotaciones.symbol[i + 3] == ')':
                    # Guardar el grupo completo
                    for j in range(4):
                        idx = i + j
                        tiempo = anotaciones.sample[idx] / anotaciones.fs
                        time_str = f"{tiempo:.3f}"
                        sample = anotaciones.sample[idx]
                        tipo = anotaciones.symbol[idx]
                        writer.writerow([time_str, sample, tipo])
                    i += 4

                # Patrón ( t )
                elif simbolo1 == '(' and simbolo2 == 't' and simbolo3 == ')':
                    # Guardar el grupo completo
                    for j in range(3):
                        idx = i + j
                        tiempo = anotaciones.sample[idx] / anotaciones.fs
                        time_str = f"{tiempo:.3f}"
                        sample = anotaciones.sample[idx]
                        tipo = anotaciones.symbol[idx]
                        writer.writerow([time_str, sample, tipo])
                    i += 3
                
                # Patrón ( t t )
                elif i < len(anotaciones.sample) - 3 and simbolo1 == '(' and simbolo2 == 't' and simbolo3 == 't' and anotaciones.symbol[i + 3] == ')':
                    # Guardar el grupo completo
                    for j in range(4):
                        idx = i + j
                        tiempo = anotaciones.sample[idx] / anotaciones.fs
                        time_str = f"{tiempo:.3f}"
                        sample = anotaciones.sample[idx]
                        tipo = anotaciones.symbol[idx]
                        writer.writerow([time_str, sample, tipo])
                    i += 4
                else:
                    i += 1
        
        return True
    except Exception as e:
        print(f"Error procesando {ruta_base}: {str(e)}")
        return False

def main():
    # Crear directorio de anotaciones si no existe
    if not os.path.exists('annotations'):
        os.makedirs('annotations')

    # Obtener todas las carpetas en QT_Database
    carpetas = [d for d in os.listdir('QT_Database') if os.path.isdir(os.path.join('QT_Database', d))]
    
    print("Procesando anotaciones...")
    exitosos = 0
    fallidos = []

    for carpeta in tqdm(carpetas, desc="Procesando carpetas"):
        ruta_base = os.path.join('QT_Database', carpeta, carpeta)
        archivo_pu = ruta_base + '.pu'
        
        if os.path.exists(archivo_pu):
            if procesar_anotaciones(ruta_base, archivo_pu):
                exitosos += 1
            else:
                fallidos.append(carpeta)
        else:
            print(f"No se encontró el archivo .pu para {carpeta}")
            fallidos.append(carpeta)

    # Mostrar resumen
    print("\nResumen del procesamiento:")
    print(f"Total de carpetas procesadas: {len(carpetas)}")
    print(f"Procesamiento exitoso: {exitosos}")
    print(f"Procesamiento fallido: {len(fallidos)}")

    if fallidos:
        print("\nCarpetas que fallaron:")
        for carpeta in fallidos:
            print(f"- {carpeta}")

if __name__ == "__main__":
    main() 