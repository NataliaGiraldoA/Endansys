# Endansys — Clasificador de Especies en Peligro de Extinción

Endansys es un modelo de clasificación de imágenes basado en deep learning que identifica especies animales y determina si se encuentran en peligro de extinción. Fue entrenado con un dataset personalizado de imágenes organizadas por especie y estado de conservación.

---

## Descripción

El proyecto utiliza una red neuronal convolucional (CNN) entrenada con Keras/TensorFlow para clasificar imágenes de animales. El modelo aprende a distinguir entre distintas especies y predice si cada una está catalogada como **en peligro** o **no en peligro**, a partir de la estructura de carpetas del dataset de entrenamiento.

---

## Estructura del repositorio

```
Endansys/
│
├── datasetN/                        # Dataset de imágenes por especie
├── modelo.ipynb                     # Notebook principal: entrenamiento y evaluación del modelo
├── model (1).ipynb                  # Versión alternativa del notebook
├── animal_species_classifier.h5     # Modelo entrenado (pesos guardados)
├── class_indices.json               # Mapeo de índices a nombres de clases
├── etiquetas_animales.csv           # CSV generado con rutas, especie y estado de conservación
├── etiquetas.py                     # Script para generar el CSV de etiquetas desde el dataset
├── renombrar.py                     # Script utilitario para renombrar archivos del dataset
└── hola.py                          # Script de prueba
```

---

## Tecnologías utilizadas

- **Python 3**
- **TensorFlow / Keras** — construcción y entrenamiento del modelo CNN
- **Jupyter Notebook** — experimentación y visualización
- **NumPy / Pandas** — procesamiento de datos
- **CSV** — etiquetado estructurado del dataset

---

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/NataliaGiraldoA/Endansys.git
cd Endansys
```

2. Instala las dependencias:

```bash
pip install tensorflow numpy pandas matplotlib jupyter
```

3. Abre el notebook principal:

```bash
jupyter notebook modelo.ipynb
```

---

## Preparación del dataset

El dataset debe estar organizado en carpetas dentro de un directorio `dataset/training/`, donde el nombre de cada carpeta indica la especie. Las carpetas cuyo nombre incluye `_peligro` son etiquetadas automáticamente como especies en peligro de extinción.

Ejemplo de estructura:

```
dataset/
└── training/
    ├── jaguar_peligro/
    ├── aguila_arpía_peligro/
    ├── venado/
    └── zorro/
```

Para generar el archivo `etiquetas_animales.csv` a partir del dataset:

```bash
python etiquetas.py
```

---

## Uso del modelo

El archivo `animal_species_classifier.h5` contiene el modelo ya entrenado. Puede cargarse directamente para realizar predicciones sin necesidad de reentrenar:

```python
from tensorflow.keras.models import load_model
import json

model = load_model("animal_species_classifier.h5")

with open("class_indices.json") as f:
    class_indices = json.load(f)
```
