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

# Guardar las anotaciones N, t y sus paréntesis en el CSV
csv_filename = 'annotations.csv'
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

print(f"\nCSV guardado como '{csv_filename}'")

# Verificar el contenido del archivo guardado
print("\nVerificando datos del archivo CSV guardado:")
try:
    with open(csv_filename, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)  # Leer encabezados
        
        # Contadores para verificación
        total_registros = 0
        tipo_inicio = 0
        tipo_n = 0
        tipo_t = 0
        tipo_fin = 0
        
        for row in csv_reader:
            total_registros += 1
            if row[2] == '(': tipo_inicio += 1
            elif row[2] == 'N': tipo_n += 1
            elif row[2] == 't': tipo_t += 1
            elif row[2] == ')': tipo_fin += 1
        
        print(f"Total de registros en CSV: {total_registros}")
        print(f"Anotaciones de inicio '(': {tipo_inicio}")
        print(f"Anotaciones tipo 'N': {tipo_n}")
        print(f"Anotaciones tipo 't': {tipo_t}")
        print(f"Anotaciones de fin ')': {tipo_fin}")
        
except Exception as e:
    print(f"Error al verificar el archivo CSV: {e}")

# Mostrar tamaño del archivo
try:
    file_size = os.path.getsize(csv_filename)
    print(f"\nTamaño del archivo CSV: {file_size} bytes")
except Exception as e:
    print(f"Error al obtener el tamaño del archivo: {e}")
