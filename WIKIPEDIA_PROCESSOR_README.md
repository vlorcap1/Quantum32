# Wikipedia Data Processor para Quantum32

## Descripción

Este módulo permite extraer, procesar y convertir artículos de Wikipedia en representaciones numéricas (vectores TF-IDF) que pueden ser utilizadas en simulaciones cuánticas del sistema Quantum32.

## Características

- **Extracción de Artículos**: Obtiene contenido completo de Wikipedia usando `wikipedia-api`
- **Procesamiento de Texto**:
  - Limpieza automática de texto (URLs, referencias, caracteres especiales)
  - Tokenización inteligente
  - Vectorización TF-IDF para conversión texto → números
  - Normalización de vectores (útil para simulaciones cuánticas)
- **Exportación Multi-formato**:
  - `.npy` - Matrices NumPy para carga rápida en simulaciones
  - `.csv` - Datos tabulares para análisis en Excel/Python
  - `.json` - Metadata y artículos completos
  - `.txt` - Lista de términos importantes

## Instalación

### Dependencias

Instala todas las dependencias requeridas:

```bash
pip install -r requirements.txt
```

O instala individualmente:

```bash
pip install wikipedia-api scikit-learn pandas
```

## Uso

### Modo Interactivo (Recomendado para principiantes)

Ejecuta el script directamente:

```bash
python wikipedia_processor.py
```

El script te guiará paso a paso:
1. Seleccionar idioma (español por defecto)
2. Configurar número de features TF-IDF
3. Ingresar títulos de artículos
4. Exportar resultados automáticamente

### Modo Programático (Para scripts y automatización)

```python
from wikipedia_processor import WikipediaProcessor

# Crear procesador
processor = WikipediaProcessor(
    language='es',           # Idioma: 'es', 'en', etc.
    max_features=100,        # Número de términos importantes a extraer
    output_dir='mis_datos'   # Directorio de salida
)

# Procesar artículos
articulos = ['Mecánica cuántica', 'Computación cuántica', 'Física cuántica']
data = processor.process_articles(articulos)

# Exportar datos
archivos = processor.export_data(data, base_filename='articulos_quantum')

# Análisis: obtener términos más relevantes por artículo
top_features = processor.get_top_features_per_article(data, top_n=10)
for titulo, terminos in top_features.items():
    print(f"\n{titulo}:")
    for termino, score in terminos:
        print(f"  - {termino}: {score:.4f}")
```

### Cargar Datos en Simulaciones

Una vez exportados los datos, puedes cargarlos en tus simulaciones:

```python
import numpy as np
import pandas as pd

# Cargar matriz TF-IDF (formato binario rápido)
tfidf_matrix = np.load('wikipedia_data/articulos_quantum_20250102_120000_tfidf.npy')

# O cargar desde CSV (más lento pero más flexible)
df = pd.read_csv('wikipedia_data/articulos_quantum_20250102_120000_features.csv', index_col=0)
tfidf_matrix = df.values

# Usar en tu simulación
print(f"Forma de la matriz: {tfidf_matrix.shape}")
print(f"Artículos: {tfidf_matrix.shape[0]}")
print(f"Features: {tfidf_matrix.shape[1]}")
```

## Ejemplos

### Ejemplo 1: Artículos de Física Cuántica

```python
from wikipedia_processor import WikipediaProcessor

processor = WikipediaProcessor(language='es', max_features=50)

articulos = [
    'Mecánica cuántica',
    'Entrelazamiento cuántico',
    'Superposición cuántica',
    'Computación cuántica',
    'Qubit'
]

data = processor.process_articles(articulos)
processor.export_data(data, 'fisica_cuantica')
```

### Ejemplo 2: Comparar Artículos en Diferentes Idiomas

```python
# Artículos en español
proc_es = WikipediaProcessor(language='es', max_features=100)
data_es = proc_es.process_articles(['Computación cuántica'])

# Artículos en inglés
proc_en = WikipediaProcessor(language='en', max_features=100)
data_en = proc_en.process_articles(['Quantum computing'])

# Comparar dimensiones
print(f"ES: {data_es['tfidf_matrix'].shape}")
print(f"EN: {data_en['tfidf_matrix'].shape}")
```

### Ejemplo 3: Análisis de Similitud

```python
from sklearn.metrics.pairwise import cosine_similarity

processor = WikipediaProcessor(language='es')
articulos = ['Gato de Schrödinger', 'Mecánica cuántica', 'Física clásica']
data = processor.process_articles(articulos)

# Calcular similitud entre artículos
similitud = cosine_similarity(data['tfidf_matrix'])

print("\nMatriz de similitud:")
for i, titulo_i in enumerate(articulos):
    for j, titulo_j in enumerate(articulos):
        print(f"{titulo_i} <-> {titulo_j}: {similitud[i][j]:.3f}")
```

## Estructura de Datos de Salida

### `tfidf_matrix` (NumPy array)
- Forma: `(n_articles, n_features)`
- Valores: Scores TF-IDF normalizados (0.0 a 1.0)
- Cada fila representa un artículo
- Cada columna representa un término importante

### `feature_names` (List)
- Lista de términos extraídos del corpus
- Ordenados por índice de columna en la matriz

### `metadata` (Dict)
Contiene:
- `n_articles`: Número de artículos procesados
- `n_features`: Número de términos (columnas)
- `article_titles`: Lista de títulos de artículos
- `vectorizer_params`: Parámetros usados en vectorización
- `processed_at`: Timestamp del procesamiento

## Integración con Quantum32

Los vectores TF-IDF generados pueden usarse como:

1. **Estados de entrada para simulaciones cuánticas**: Los vectores normalizados pueden representar estados cuánticos iniciales
2. **Datos de entrenamiento**: Para algoritmos de optimización cuántica como QAOA
3. **Benchmarks**: Comparar rendimiento de diferentes configuraciones del sistema
4. **Encoding de información**: Los bits del vector pueden mapearse a qubits virtuales

### Ejemplo de integración

```python
# Cargar datos procesados
import numpy as np
tfidf_matrix = np.load('wikipedia_data/quantum_articles_tfidf.npy')

# Convertir a representación binaria para qubits
# (discretizar valores continuos a bits)
threshold = np.median(tfidf_matrix)
binary_matrix = (tfidf_matrix > threshold).astype(int)

# Usar en simulación Quantum32
# Por ejemplo, enviar al ESP32 vía serial
for article_bits in binary_matrix:
    # Preparar datos para envío
    bitstring = ''.join(map(str, article_bits[:16]))  # Primeros 16 bits
    print(f"Enviar a ESP32: {bitstring}")
```

## Beneficios

- **Transformación automática** de texto en datos numéricos interpretables
- **Formato compatible** con herramientas científicas estándar (NumPy, Pandas)
- **Escalable**: Procesa desde 1 hasta cientos de artículos
- **Reproducible**: Metadata completa de cada procesamiento
- **Flexible**: Exporta en múltiples formatos para diferentes usos

## Troubleshooting

### Error: "wikipedia-api no está instalada"
```bash
pip install wikipedia-api
```

### Error: "Artículo no encontrado"
- Verifica el título exacto en Wikipedia
- Intenta con diferentes variaciones (con/sin tildes, mayúsculas)
- Usa el buscador de Wikipedia primero para confirmar el título

### Matriz muy sparse (muchos ceros)
- Aumenta `max_features` para capturar más términos
- Reduce `min_df` en TfidfVectorizer (para incluir términos más raros)
- Procesa más artículos relacionados para tener un corpus más rico

### Memoria insuficiente
- Reduce `max_features`
- Procesa artículos en batches más pequeños
- Usa artículos más cortos

## Notas Técnicas

### TF-IDF (Term Frequency - Inverse Document Frequency)

El algoritmo TF-IDF evalúa la importancia de un término en un documento:

- **TF**: Frecuencia del término en el documento
- **IDF**: Rareza del término en el corpus (penaliza términos comunes)

Un score alto indica que el término es:
- Frecuente en el documento actual
- Raro en el corpus general
- Por tanto, **característico** de ese documento

### Normalización L2

Los vectores se normalizan usando norma L2 (euclidiana):
```
v_normalized = v / ||v||₂
```

Esto garantiza que:
- Todos los vectores tienen magnitud 1
- Se preservan ángulos entre vectores
- Útil para calcular similitud coseno y comparar estados

## Autor

Basado en el sistema Quantum32 Hybrid Sampler

## Licencia

CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0 International)

## Contribuciones

Las mejoras son bienvenidas. Áreas de interés:
- [ ] Soporte para más idiomas automáticamente
- [ ] Caché de artículos para evitar re-descargas
- [ ] Visualizaciones de similitud entre artículos
- [ ] Export directo a formato Quantum32 binary
- [ ] Integración con otros procesadores de texto (spaCy, NLTK)
