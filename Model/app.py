import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Cargar el modelo de clasificación
model = tf.keras.models.load_model('modelo_clasificador_onda_r.keras')

# Cargar los datos de prueba
with open('test.json', 'r') as f:
    data = json.load(f)

X = np.array(data['normalized_waves'])
y = np.array(data['tags'])

# Estado para el índice actual
idx = [0]  # Usamos una lista para que sea mutable en el scope de los handlers

def plot_onda(idx_actual):
    onda = X[idx_actual]
    etiqueta_real = y[idx_actual]
    onda_entrada = onda.reshape(1, -1, 1)
    prediccion = model.predict(onda_entrada, verbose=0)[0][0]
    es_r = prediccion >= 0.5
    plt.cla()
    plt.plot(onda, label='Onda')
    plt.legend()
    plt.title(
        f'Onda #{idx_actual+1} / {len(X)} | '
        f'Real: {"R" if etiqueta_real==1 else "No R"} | '
        f'Predicción: {"R" if es_r else "No R"} ({prediccion:.2f})'
    )
    plt.draw()

def on_key(event):
    if event.key == 'right':
        idx[0] = (idx[0] + 1) % len(X)
        plot_onda(idx[0])
    elif event.key == 'left':
        idx[0] = (idx[0] - 1) % len(X)
        plot_onda(idx[0])

fig = plt.figure()
plot_onda(idx[0])
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()
