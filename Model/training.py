import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, Flatten
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Cargar los datos del JSON
with open('all_waves_data.json', 'r') as f:
    data = json.load(f)

# Extraer todas las ondas y etiquetas de todos los archivos
all_waves = []
all_tags = []

for archivo in data['datos']:
    all_waves.extend(archivo['normalized_waves'])
    all_tags.extend(archivo['tags'])

# Convertir a arrays de numpy
X = np.array(all_waves)
y = np.array(all_tags)

print(f"Total de ondas para entrenamiento: {len(X)}")
print(f"Distribución de etiquetas: {np.bincount(y)}")

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Reshape para CNN 1D
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Modelo simplificado para microcontrolador
model = Sequential([
    Conv1D(16, 3, activation='relu', input_shape=(X_train.shape[1], 1)),
    MaxPooling1D(2),
    Flatten(),
    Dense(1, activation='sigmoid')
])

# Compilar el modelo
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Entrenamiento con early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

# Entrenar el modelo
history = model.fit(
    X_train, y_train,
    epochs=20,  # Reducido el número de épocas
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=1
)

# Evaluar
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f'Accuracy en el conjunto de prueba: {acc:.4f}')

# Mostrar resumen del modelo
model.summary()

# Guardar el modelo
model.save('modelo_clasificador_onda_r.keras')

# Guardar el historial de entrenamiento
plt.figure(figsize=(12, 4))

# Gráfico de accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Entrenamiento')
plt.plot(history.history['val_accuracy'], label='Validación')
plt.title('Accuracy durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Accuracy')
plt.legend()

# Gráfico de pérdida
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Entrenamiento')
plt.plot(history.history['val_loss'], label='Validación')
plt.title('Pérdida durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Pérdida')
plt.legend()

plt.tight_layout()
plt.savefig('historial_entrenamiento.png')
plt.close()
