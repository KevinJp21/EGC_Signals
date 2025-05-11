import wfdb
import numpy as np
import pandas as pd
import json
import os
from tqdm import tqdm

def procesar_archivo_qt(ruta_base, archivo_anotaciones):
    try:
        # Leer el registro ECG
        record = wfdb.rdrecord(ruta_base)
        fs = record.fs
        ecgsignal = record.p_signal[:, 0]
        timeaxis = np.arange(len(ecgsignal)) / fs

        # Cargar anotaciones
        annotations_df = pd.read_csv(archivo_anotaciones)

        # Extraer ondas centradas en cada anotación
        ondas_normalizadas = []
        tags = []
        duracion_estandar = 0.120
        longitud_estandar = int(duracion_estandar * fs)
        mitad_ventana = longitud_estandar // 2

        for _, row in annotations_df.iterrows():
            tipo = str(row['Type']).upper()
            centro = int(round(row['Time'] * fs))
            start = max(0, centro - mitad_ventana)
            end = min(len(ecgsignal), centro + mitad_ventana)
            onda = ecgsignal[start:end]
            
            # Padding si la onda es más corta que la longitud estándar
            if len(onda) < longitud_estandar:
                onda = np.pad(onda, (0, longitud_estandar - len(onda)), 'constant', constant_values=(0, 0))
            
            # Normalización
            A = np.max(onda)
            B = np.min(onda)
            if A == B:
                normalized_wave = np.zeros_like(onda)
            else:
                normalized_wave = (onda - B) / (A - B)
            
            ondas_normalizadas.append(normalized_wave.tolist())
            
            # Tag: 1 si es N o NN, 0 en otro caso
            if tipo in ['N', 'NN']:
                tags.append(1)
            else:
                tags.append(0)

        return {
            'normalized_waves': ondas_normalizadas,
            'tags': tags,
            'metadata': {
                'frecuencia_muestreo': float(fs),
                'source': os.path.basename(ruta_base),
                'total_ondas': len(ondas_normalizadas),
                'ondas_r': sum(tags),
                'otras_ondas': len(tags) - sum(tags)
            }
        }
    except Exception as e:
        print(f"Error procesando {ruta_base}: {str(e)}")
        return None

def main():
    # Crear directorio para el JSON si no existe
    if not os.path.exists('processed_data'):
        os.makedirs('processed_data')

    # Obtener todas las carpetas en QT_Database
    carpetas = [d for d in os.listdir('QT_Database') if os.path.isdir(os.path.join('QT_Database', d))]
    
    print("Procesando archivos QT y anotaciones...")
    datos_completos = []
    fallidos = []

    for carpeta in tqdm(carpetas, desc="Procesando archivos"):
        ruta_base = os.path.join('QT_Database', carpeta, carpeta)
        archivo_anotaciones = os.path.join('annotations', f'{carpeta}.csv')
        
        if os.path.exists(archivo_anotaciones):
            resultado = procesar_archivo_qt(ruta_base, archivo_anotaciones)
            if resultado:
                datos_completos.append(resultado)
            else:
                fallidos.append(carpeta)
        else:
            print(f"No se encontró el archivo de anotaciones para {carpeta}")
            fallidos.append(carpeta)

    # Guardar todos los datos en un único JSON
    if datos_completos:
        with open('processed_data/all_waves_data.json', 'w') as f:
            json.dump({
                'datos': datos_completos,
                'resumen': {
                    'total_archivos_procesados': len(datos_completos),
                    'archivos_fallidos': len(fallidos),
                    'total_ondas': sum(d['metadata']['total_ondas'] for d in datos_completos),
                    'total_ondas_r': sum(d['metadata']['ondas_r'] for d in datos_completos),
                    'total_otras_ondas': sum(d['metadata']['otras_ondas'] for d in datos_completos)
                }
            }, f, indent=4)

        print("\nResumen del procesamiento:")
        print(f"Total de archivos procesados: {len(datos_completos)}")
        print(f"Archivos fallidos: {len(fallidos)}")
        if fallidos:
            print("\nArchivos que fallaron:")
            for carpeta in fallidos:
                print(f"- {carpeta}")
        
        print("\nDatos guardados en: processed_data/all_waves_data.json")
    else:
        print("No se procesó ningún archivo correctamente.")

if __name__ == "__main__":
    main() 