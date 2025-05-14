import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, Flatten
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

# Crear directorio para métricas si no existe
if not os.path.exists('metrics'):
    os.makedirs('metrics')

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
    epochs=20,
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

# Después de entrenar y evaluar, agregamos el análisis detallado de métricas
y_pred = model.predict(X_test)
y_pred_binary = (y_pred > 0.5).astype(int)

# Calcular métricas
metrics_dict = {
    'accuracy': acc,
    'f1_score': f1_score(y_test, y_pred_binary),
    'precision': precision_score(y_test, y_pred_binary),
    'recall': recall_score(y_test, y_pred_binary)
}

# Guardar métricas en CSV
metrics_df = pd.DataFrame([metrics_dict])
metrics_df.to_csv('metrics/model_metrics.csv', index=False)

# Generar y guardar reporte de clasificación
classification_rep = classification_report(y_test, y_pred_binary)
with open('metrics/classification_report.txt', 'w') as f:
    f.write(classification_rep)

# Crear y guardar matriz de confusión
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred_binary)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Matriz de Confusión')
plt.ylabel('Verdadero')
plt.xlabel('Predicho')
plt.savefig('metrics/confusion_matrix.png')
plt.close()

# Graficar curva ROC
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_test, y_pred)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Tasa de Falsos Positivos')
plt.ylabel('Tasa de Verdaderos Positivos')
plt.title('Curva ROC')
plt.legend(loc="lower right")
plt.savefig('metrics/roc_curve.png')
plt.close()

# Graficar métricas durante el entrenamiento
plt.figure(figsize=(15, 5))

# Gráfico de accuracy
plt.subplot(1, 3, 1)
plt.plot(history.history['accuracy'], label='Entrenamiento')
plt.plot(history.history['val_accuracy'], label='Validación')
plt.title('Accuracy durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Accuracy')
plt.legend()

# Gráfico de pérdida
plt.subplot(1, 3, 2)
plt.plot(history.history['loss'], label='Entrenamiento')
plt.plot(history.history['val_loss'], label='Validación')
plt.title('Pérdida durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Pérdida')
plt.legend()

# Guardar historial de métricas
history_df = pd.DataFrame(history.history)
history_df.to_csv('metrics/training_history.csv', index=False)

plt.tight_layout()
plt.savefig('metrics/training_curves.png')
plt.close()

# Guardar un resumen general en formato JSON
summary = {
    'model_metrics': metrics_dict,
    'training_params': {
        'total_samples': len(X),
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'epochs': len(history.history['loss']),
        'batch_size': 32,
        'early_stopping_patience': 3
    },
    'class_distribution': {
        'total': len(y),
        'class_0': int(np.sum(y == 0)),
        'class_1': int(np.sum(y == 1))
    }
}

with open('metrics/training_summary.json', 'w') as f:
    json.dump(summary, f, indent=4)
