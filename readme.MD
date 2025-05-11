# Procesamiento de Señales ECG y Clasificación de Ondas R

Este proyecto realiza el procesamiento de señales ECG y la clasificación de ondas R usando Python y TensorFlow. El objetivo es detectar y clasificar ondas R en registros ECG, procesar los datos y entrenar un modelo de clasificación ligero para microcontroladores.

## Flujo de Trabajo

1. **Procesamiento de Señales** (`Process_Waves/process_waves.py`)
   - Carga señales ECG del conjunto de datos QT Database
   - Detecta y extrae ondas R
   - Normaliza las amplitudes
   - Genera etiquetas binarias
   - Guarda los datos procesados en formato JSON

2. **Entrenamiento del Modelo** (`Model/training.py`)
   - Carga los datos procesados
   - Entrena un modelo CNN 1D ligero
   - Evalúa el rendimiento del modelo
   - Guarda el modelo entrenado
   - Genera gráficos de entrenamiento

## Estructura del Proyecto

```
.
├── Process_Waves/
│   ├── process_waves.py    # Script de procesamiento
│   ├── all_waves_data.json # Datos procesados
│   └── .gitignore
├── Model/
│   ├── training.py         # Script de entrenamiento
│   ├── modelo_clasificador_onda_r.keras  # Modelo entrenado
│   └── historial_entrenamiento.png       # Gráficos de entrenamiento
├── QT_Database/           # Carpeta con archivos ECG
└── README.md             # Este archivo
```

## Estructura de Datos

### all_waves_data.json
```json
{
  "datos": [
    {
      "normalized_waves": [...],
      "tags": [...],
      "metadata": {
        "frecuencia_muestreo": float,
        "source": "nombre_archivo",
        "total_ondas": int,
        "ondas_r": int,
        "otras_ondas": int
      }
    }
  ],
  "resumen": {
    "total_archivos_procesados": int,
    "archivos_fallidos": int,
    "total_ondas": int,
    "total_ondas_r": int,
    "total_otras_ondas": int
  }
}
```

## Modelo de Clasificación

El modelo implementado es una CNN 1D ligera, optimizada para microcontroladores:

```python
model = Sequential([
    Conv1D(16, 3, activation='relu', input_shape=(X_train.shape[1], 1)),
    MaxPooling1D(2),
    Flatten(),
    Dense(1, activation='sigmoid')
])
```

Características del modelo:
- Arquitectura minimalista (2 capas principales)
- Optimizado para microcontroladores
- Entrenamiento con early stopping
- 20 épocas máximas
- Batch size de 32

## Uso

1. **Procesar las señales**:
   ```bash
   cd Process_Waves
   python process_waves.py
   ```

2. **Entrenar el modelo**:
   ```bash
   cd Model
   python training.py
   ```

## Requisitos

Crear y activar el entorno virtual:
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux/Mac
```

Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Dependencias Principales
- tensorflow
- numpy
- matplotlib
- scikit-learn
- wfdb
- pandas

## Notas
- El modelo está optimizado para ser ligero y eficiente
- Los datos se normalizan para mejorar el entrenamiento
- Se incluye early stopping para evitar sobreentrenamiento
- Los resultados del entrenamiento se guardan en gráficos
- El modelo final se guarda en formato .keras

# Creación de Entorno Virtual e Instalación de Dependencias

Este documento explica cómo crear un entorno virtual en Python e instalar las dependencias necesarias para ejecutar el código correctamente.

## 1. Crear un Entorno Virtual

Python proporciona la herramienta `venv` para crear entornos virtuales y evitar conflictos con dependencias instaladas de forma global en el dispositivo. Para configurarlo, sigue estos pasos:

### En Windows (CMD o PowerShell):
```sh
python -m venv venv
```

Para activar el entorno:
```sh
.\.venv\Scripts\activate
```

### En macOS y Linux:
```sh
python3 -m venv venv
```

Para activar el entorno:
```sh
source ./venv/bin/activate
```

---

## 2. Instalar Dependencias

Dentro del entorno virtual activado, instala las dependencias necesarias ejecutando:

```sh
pip install -r requirements.txt
```

---

## 3. Ejecutar

Para procesar los datos:
```sh
python appCeldas.py
```

Para visualizar los resultados:
```sh
python visualizar_datos.py
```

Usa tu IDE favorito para ejecutar las celdas individualmente y explorar los datos interactivamente.

---
## Estructira del archvio all_waves_data.json
```sh
   {
     "datos": [
       {
         "normalized_waves": [...],
         "tags": [...],
         "metadata": {
           "frecuencia_muestreo": float,
           "source": "nombre_archivo",
           "total_ondas": int,
           "ondas_r": int,
           "otras_ondas": int
         }
       },
       ...
     ],
     "resumen": {
       "total_archivos_procesados": int,
       "archivos_fallidos": int,
       "total_ondas": int,
       "total_ondas_r": int,
       "total_otras_ondas": int
     }
   }
 ```
