### Análisis de la Matriz de Confusión

|                | Predicho 0 | Predicho 1 |
|----------------|------------|------------|
| **Verdadero 0**|   206426   |    3235    |
| **Verdadero 1**|    4145    |   40161    |

#### Definiciones
- **Verdadero 0 (Clase 0):** Ejemplos negativos reales (no onda R)
- **Verdadero 1 (Clase 1):** Ejemplos positivos reales (onda R)
- **Predicho 0:** El modelo predijo clase 0
- **Predicho 1:** El modelo predijo clase 1

#### Interpretación de los valores
- **206426 (TN):** Verdaderos negativos (el modelo predijo correctamente la clase 0)
- **40161 (TP):** Verdaderos positivos (el modelo predijo correctamente la clase 1)
- **3235 (FP):** Falsos positivos (el modelo predijo clase 1, pero era clase 0)
- **4145 (FN):** Falsos negativos (el modelo predijo clase 0, pero era clase 1)

---

### **Análisis general**

- El modelo tiene un **muy buen desempeño general** (accuracy alto).
- **Precisión (Tasa falsol positivos) y recall (Tasa falsos negativos) para la clase 1** (ondas R) son altos, lo que significa que el modelo rara vez se equivoca al predecir una onda R y detecta la mayoría de las ondas R reales.
- El número de **falsos negativos** (ondas R no detectadas) es bajo en comparación con los verdaderos positivos.
- El número de **falsos positivos** (predice onda R cuando no lo es) también es bajo.