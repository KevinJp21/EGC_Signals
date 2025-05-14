import wfdb
import os
import csv
from tqdm import tqdm

def es_letra(caracter):
    return caracter.isalpha()

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
            while i < len(anotaciones.sample):
                if i < len(anotaciones.sample) - 2:  # Asegurarse de que hay suficientes símbolos para procesar
                    if anotaciones.symbol[i] == '(':
                        # Buscar el paréntesis de cierre
                        j = i + 1
                        letras_encontradas = []
                        nuevo_inicio = None
                        
                        # Recolectar todas las letras hasta encontrar el paréntesis de cierre
                        while j < len(anotaciones.sample) and anotaciones.symbol[j] != ')':
                            if anotaciones.symbol[j] == '(':
                                nuevo_inicio = j
                                break
                            if es_letra(anotaciones.symbol[j]):
                                letras_encontradas.append(j)
                            j += 1
                        
                        # Si encontramos un nuevo paréntesis de inicio
                        if nuevo_inicio is not None:
                            i = nuevo_inicio
                            continue
                            
                        # Si encontramos el patrón válido (paréntesis, letras, paréntesis)
                        if j < len(anotaciones.sample) and anotaciones.symbol[j] == ')' and letras_encontradas:
                            # Guardar todo el grupo incluyendo paréntesis
                            for idx in range(i, j + 1):
                                tiempo = anotaciones.sample[idx] / anotaciones.fs
                                time_str = f"{tiempo:.3f}"
                                sample = anotaciones.sample[idx]
                                tipo = anotaciones.symbol[idx]
                                writer.writerow([time_str, sample, tipo])
                            i = j + 1
                            continue
                
                # Si no se encontró un patrón válido, avanzar al siguiente símbolo
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