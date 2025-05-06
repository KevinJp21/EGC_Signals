import wfdb
import os
import csv

# Ruta al archivo base (sin extensión)
base = './QT_Database/sel102/sel102'

# Verificar si existe el archivo de anotaciones
ruta_q1c = base + '.pu'
if not os.path.exists(ruta_q1c):
    print(f'No se encontró el archivo: {ruta_q1c}')
    exit(1)

# Leer las anotaciones usando wfdb.rdann
anotaciones = wfdb.rdann(base, 'pu')

# Guardar todas las anotaciones en el CSV
csv_filename = 'ondas_R.csv'
with open(csv_filename, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'Sample #', 'Type'])  # encabezado

    for idx in range(len(anotaciones.sample)):
        tiempo = anotaciones.sample[idx] / anotaciones.fs
        time_str = f"{tiempo:.3f}"
        sample = anotaciones.sample[idx]
        tipo = anotaciones.symbol[idx]
        writer.writerow([time_str, sample, tipo])

print(f"\nCSV guardado como '{csv_filename}'")
print(f"Total de anotaciones guardadas: {len(anotaciones.sample)}")

# Verificar el contenido del archivo guardado
print("\nVerificando datos del archivo CSV guardado:")
try:
    with open(csv_filename, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)  # Leer encabezados
        
        # Contadores para verificación
        total_registros = 0
        tipo_inicio = 0
        tipo_pico = 0 
        tipo_pico_nn = 0
        tipo_fin = 0
        
        for row in csv_reader:
            total_registros += 1
            if row[2] == '(': tipo_inicio += 1
            elif row[2] == 'N': tipo_pico += 1
            elif row[2] == ')': tipo_fin += 1
        
        # Calcular ondas completas considerando ambos patrones
        ondas_completas = min(tipo_inicio, tipo_fin, tipo_pico // 1)  # Puede haber 1 o 2 picos por onda
        
        print(f"Total de registros en CSV: {total_registros}")
        print(f"Anotaciones de inicio '(': {tipo_inicio}")
        print(f"Anotaciones de pico 'N': {tipo_pico}")
        print(f"Anotaciones de fin ')': {tipo_fin}")
        print(f"Ondas R completas (tríos o cuartetos): {ondas_completas}")
        
        # Verificar coherencia
        if ondas_completas != total_registros:
            print("ADVERTENCIA: Inconsistencia en el conteo de ondas R")
            
except Exception as e:
    print(f"Error al verificar el archivo CSV: {e}")

# Mostrar tamaño del archivo
try:
    file_size = os.path.getsize(csv_filename)
    print(f"\nTamaño del archivo CSV: {file_size} bytes")
except Exception as e:
    print(f"Error al obtener el tamaño del archivo: {e}")
