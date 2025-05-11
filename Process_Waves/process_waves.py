#%% Importación de librerías
import wfdb
import matplotlib
matplotlib.use('TkAgg')  # Configurar el backend interactivo
import matplotlib.pyplot as plt
plt.ion()  # Activar modo interactivo
import numpy as np
import pandas as pd
import json
from datetime import datetime

#%% Configuración inicial y carga de datos
# Ruta del archivo de registro ECG
record_name = r"./QT_Database/sel102/sel102"

# Leer el registro ECG
record = wfdb.rdrecord(record_name)

# Obtener la frecuencia de muestreo
fs = record.fs  

# Extraer todo el canal de ECG
ecgsignal = record.p_signal[:, 0]

# Crear el eje de tiempo
timeaxis = np.arange(len(ecgsignal)) / fs

#%% Cargar y procesar el archivo CSV con anotaciones de ondas R
# Cargar el archivo CSV con las anotaciones
annotations_df = pd.read_csv('annotations.csv')

# Extraer ondas centradas en cada anotación
ondas_estandarizadas = []
ondas_normalizadas = []
tiempos_estandarizados = []
tags = []
start_indices = []
end_indices = []
r_peaks_calculados = []

duracion_estandar = 0.120
longitud_estandar = int(duracion_estandar * fs)
mitad_ventana = longitud_estandar // 2

for idx, row in annotations_df.iterrows():
    tipo = str(row['Type']).upper()
    centro = int(round(row['Time'] * fs))
    start = max(0, centro - mitad_ventana)
    end = min(len(ecgsignal), centro + mitad_ventana)
    onda = ecgsignal[start:end]
    tiempo = timeaxis[start:end]
    # Padding si la onda es más corta que la longitud estándar
    if len(onda) < longitud_estandar:
        onda = np.pad(onda, (0, longitud_estandar - len(onda)), 'constant', constant_values=(0, 0))
        tiempo = np.pad(tiempo, (0, longitud_estandar - len(tiempo)), 'constant', constant_values=(0, 0))
    ondas_estandarizadas.append(onda)
    tiempos_estandarizados.append(tiempo)
    # Normalización
    A = np.max(onda)
    B = np.min(onda)
    if A == B:
        normalized_wave = np.zeros_like(onda)
    else:
        normalized_wave = (onda - B) / (A - B)
    ondas_normalizadas.append(normalized_wave)
    # Tag: 1 si es N o NN, 0 en otro caso
    if tipo in ['N', 'NN']:
        tags.append(1)
    else:
        tags.append(0)
    start_indices.append(start)
    end_indices.append(end)
    # Pico máximo local
    if len(onda) > 0:
        r_peaks_calculados.append(start + np.argmax(onda))
    else:
        r_peaks_calculados.append(start)

# Convertir a arrays de numpy
ondas_estandarizadas = np.array(ondas_estandarizadas, dtype=object)
ondas_normalizadas = np.array(ondas_normalizadas, dtype=object)
tiempos_estandarizados = np.array(tiempos_estandarizados, dtype=object)
tags = np.array(tags)
start_indices = np.array(start_indices)
end_indices = np.array(end_indices)
r_peaks_calculados = np.array(r_peaks_calculados)

print(f"\nDistribución de tags:")
print(f"Total de ondas: {len(tags)}")
print(f"Ondas con anotación 'N' o 'NN': {np.sum(tags)}")
print(f"Ondas con otras anotaciones: {len(tags) - np.sum(tags)}")

#%% Visualización interactiva de ondas R normalizadas
def visualizar_onda_normalizada(index):
    if not plt.get_fignums():
        global fig_norm, ax_norm
        fig_norm, ax_norm = plt.subplots(figsize=(10, 6))
        fig_norm.canvas.mpl_connect("key_press_event", on_key_normalizada)
    ax_norm.clear()
    # Graficar la onda normalizada
    ax_norm.plot(tiempos_estandarizados[index], 
                ondas_normalizadas[index], 
                color='c', linewidth=2, label='Señal')
    ax_norm.set_title(f'Onda R normalizada {index+1} de {len(ondas_normalizadas)}\n'
                     f'Duración: {tiempos_estandarizados[index][-1] - tiempos_estandarizados[index][0]:.2f} s')
    ax_norm.set_xlabel('Tiempo (s)')
    ax_norm.set_ylabel('Amplitud Normalizada')
    ax_norm.legend()
    ax_norm.grid(True)
    plt.draw()
    plt.pause(0.1)
    print(f"\n📊 Datos de la Onda R normalizada {index+1}:")
    print(f"Duración: {tiempos_estandarizados[index][-1] - tiempos_estandarizados[index][0]:.2f} s")
    print("Tiempo (s) -> Amplitud normalizada")
    for t, amp in zip(tiempos_estandarizados[index], 
                       ondas_normalizadas[index]):
        print(f"{t:.5f} -> {amp:.5f}")

def on_key_normalizada(event):
    global index_norm
    if event.key == "right":
        index_norm = (index_norm + 1) % len(ondas_normalizadas)
        visualizar_onda_normalizada(index_norm)
    elif event.key == "left":
        index_norm = (index_norm - 1) % len(ondas_normalizadas)
        visualizar_onda_normalizada(index_norm)

#%% Inicialización de visualización de ondas normalizadas
if len(ondas_normalizadas) > 0:
    index_norm = 0
    visualizar_onda_normalizada(index_norm)
    plt.show(block=True)
else:
    print("Error: No se encontraron ondas R para normalizar.")

#%% Visualización de todas las ondas normalizadas concatenadas
if len(ondas_normalizadas) > 0:
    plt.figure(figsize=(15, 6))
    
    # Determinar la longitud máxima para el padding
    max_len = max(len(wave) for wave in ondas_normalizadas)
    
    # Crear un array para todas las ondas con padding
    all_waves = []
    for wave in ondas_normalizadas:
        # Padding si es necesario
        padded_wave = np.pad(wave, (0, max_len - len(wave)), 'constant', constant_values=(0, 0))
        all_waves.append(padded_wave)
    
    # Concatenar todas las ondas
    full_signal = np.concatenate(all_waves)
    time_full = np.arange(len(full_signal)) / fs
    
    plt.plot(time_full, full_signal, 'b-', linewidth=1)
    plt.title('Señal ECG Concatenada de Ondas R Normalizadas (desde CSV)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud Normalizada')
    plt.grid(True)
    plt.show()
else:
    print("Error: No hay ondas normalizadas para visualizar.")

#%% Guardar los datos procesados para entrenamiento
if len(ondas_normalizadas) > 0:
    # Preparar los datos en formato JSON
    # Convertimos todo a listas para JSON
    data_json = {
        'normalized_waves': [wave.tolist() for wave in ondas_normalizadas],
        'tags': tags.tolist(),
        'metadata': {
            'frecuencia_muestreo': float(fs),
            'source': 'CSV annotations',
        }
    }
    
    with open('test.json', 'w') as f:
        json.dump(data_json, f, indent=4)
    
    print("\nResumen de los datos guardados en JSON:")
    print(f"Número total de ondas R: {len(data_json['normalized_waves'])}")
    if len(data_json['normalized_waves']) > 0:
        print(f"Dimensiones de la primera onda: {len(data_json['normalized_waves'][0])}")
    print(f"Frecuencia de muestreo: {data_json['metadata']['frecuencia_muestreo']} Hz")
    print("\nArchivo JSON creado: wave_data.json")
else:
    print("Error: No hay datos para guardar en JSON.")

# %%