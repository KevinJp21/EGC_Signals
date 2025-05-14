### Explicación de los campos en `model_metrics.csv`

El archivo `model_metrics.csv` contiene las principales métricas de evaluación del modelo de clasificación. A continuación se explica el significado de cada campo:

- **accuracy** (**Exactitud**):  
  Es la proporción de predicciones correctas (tanto positivas como negativas) sobre el total de muestras evaluadas.  
  _Ejemplo_: Un valor de **0.9709** (97%) significa que el modelo acertó el 97% de todas las predicciones realizadas.

- **f1_score** (**Puntaje F1**):  
  Es la media armónica entre la precisión y el recall. Es especialmente útil cuando hay un desbalance entre las clases, ya que combina ambas métricas en un solo valor.  
  _Ejemplo_: Un valor de **0.9159** indica un buen equilibrio entre precisión y recall.

- **precision** (**Precisión**):  
  Indica, de todas las veces que el modelo predijo la clase positiva (onda R), cuántas veces acertó realmente.  
  _Ejemplo_: Un valor de **0.9255** (92.5%) significa que, de todas las predicciones positivas, el 92.5% fueron correctas.

- **recall** (**Sensibilidad** o **Exhaustividad**):  
  Indica, de todas las verdaderas instancias positivas (ondas R reales), cuántas fueron correctamente identificadas por el modelo.  
  _Ejemplo_: Un valor de **0.9064** (90.6%) significa que el modelo detectó el 90.6% de todas las ondas R reales.

