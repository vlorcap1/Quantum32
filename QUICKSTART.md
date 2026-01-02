# Guía Rápida: Wikipedia Data Processor

## 🚀 Inicio Rápido (5 minutos)

### Paso 1: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar Ejemplos

```bash
# Ver todos los ejemplos en acción
python ejemplo_uso.py
```

### Paso 3: Usar en tu Proyecto

```python
from wikipedia_processor import WikipediaProcessor

# Crear procesador
processor = WikipediaProcessor(language='es', max_features=100)

# Procesar artículos
data = processor.process_articles(['Mecánica cuántica', 'Qubit'])

# Exportar datos
processor.export_data(data)
```

## 📖 Documentación Completa

Ver [WIKIPEDIA_PROCESSOR_README.md](WIKIPEDIA_PROCESSOR_README.md) para:
- Documentación detallada
- Ejemplos avanzados
- Integración con Quantum32
- Solución de problemas

## 🧪 Ejecutar Tests

```bash
python test_wikipedia_processor.py
```

**Nota**: Los tests requieren conexión a internet para acceder a Wikipedia.

## 📁 Archivos Incluidos

- `wikipedia_processor.py` - Módulo principal
- `requirements.txt` - Dependencias
- `ejemplo_uso.py` - Ejemplos de uso
- `test_wikipedia_processor.py` - Suite de pruebas
- `WIKIPEDIA_PROCESSOR_README.md` - Documentación completa
- `QUICKSTART.md` - Este archivo

## 🎯 Casos de Uso Principales

### 1. Preparar Datos para Simulaciones

```python
processor = WikipediaProcessor(language='es')
data = processor.process_articles(['Superposición cuántica', 'Entrelazamiento'])
processor.export_data(data, 'simulacion_quantum')
```

### 2. Análisis de Similitud

```python
from sklearn.metrics.pairwise import cosine_similarity

data = processor.process_articles(['Artículo 1', 'Artículo 2'])
similitud = cosine_similarity(data['tfidf_matrix'])
print(f"Similitud: {similitud[0,1]:.3f}")
```

### 3. Encoding Cuántico

```python
import numpy as np

data = processor.process_articles(['Qubit'])
vector = data['tfidf_matrix'][0]

# Convertir a bits
threshold = np.median(vector[vector > 0])
bits = (vector > threshold).astype(int)
print(f"Bitstring: {''.join(map(str, bits))}")
```

## 🔗 Integración con Quantum32

Los vectores TF-IDF generados pueden usarse como:

1. **Estados iniciales** para simulaciones cuánticas
2. **Datos de entrenamiento** para QAOA
3. **Benchmarks** para comparar configuraciones
4. **Encoding de información** mapeado a qubits

Ver documentación completa para más detalles.

## 💡 Tips

- Usa `max_features=50` para artículos cortos
- Usa `max_features=200` para análisis más detallados
- Los archivos `.npy` se cargan más rápido que CSV
- El idioma por defecto es español ('es')

## ❓ Problemas Comunes

### Error: "wikipedia-api no está instalada"
```bash
pip install wikipedia-api
```

### Artículo no encontrado
Verifica el título exacto en Wikipedia antes de procesarlo.

### Muy lento
Procesa menos artículos o reduce `max_features`.

## 📞 Soporte

Para problemas o preguntas, abre un issue en el repositorio de GitHub.

---

**¡Listo para usar!** 🎉
