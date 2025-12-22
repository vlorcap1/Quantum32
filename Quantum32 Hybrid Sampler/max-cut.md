# Max-Cut: Concepto y Aplicaciones en Quantum32

## ¿Qué es el Problema Max-Cut?

**Max-Cut** (Corte Máximo) es un problema clásico de **optimización combinatoria** que pertenece a la clase **NP-hard**, lo que significa que no existe un algoritmo conocido que lo resuelva de manera óptima en tiempo polinomial para todos los casos.

### Definición Formal

Dado un grafo no dirigido **G = (V, E)** con:
- **V**: Conjunto de nodos (vértices)
- **E**: Conjunto de aristas (conexiones entre nodos)

El objetivo es **particionar los nodos en dos grupos** (digamos, grupo 0 y grupo 1) de manera que se **maximice el número de aristas que cruzan entre los dos grupos**.

```
        Grupo 0              Grupo 1
       ┌───────┐            ┌───────┐
       │   A   │────────────│   B   │   ← Arista "cortada" ✓
       │   C   │            │   D   │   
       └───────┘            └───────┘
           │                    │
           └────────────────────┘        ← Arista "cortada" ✓
           
       Si A-C están en el mismo grupo, esa arista NO cuenta.
```

### Score Max-Cut

El **score** de una partición es la suma de los pesos de las aristas cortadas:

```
Score = Σ w(i,j)  para toda arista (i,j) donde color[i] ≠ color[j]
```

---

## ¿Por Qué es Importante?

### Aplicaciones Reales

1. **Diseño de Circuitos (VLSI)**
   - Minimizar conexiones entre chips separados
   - Reducir interferencia electromagnética

2. **Clustering y Machine Learning**
   - Segmentación de imágenes
   - Detección de comunidades en redes sociales

3. **Física Estadística**
   - Modelo de Ising antiferromagnético
   - Simulación de sistemas de espín

4. **Logística**
   - Partición óptima de redes de distribución
   - Balanceo de carga en servidores

---

## ¿Cómo lo Resuelve el Quantum32?

### Inspiración Cuántica

El sistema Quantum32 utiliza un enfoque **inspirado en computación cuántica** para explorar el espacio de soluciones:

1. **Ruido Controlado (T)**: Simula "fluctuaciones térmicas" que permiten escapar de mínimos locales
2. **Bias (B)**: Introduce preferencias direccionales en la búsqueda
3. **Acoplamiento (Kp)**: Correlaciona bits vecinos, similar al acoplamiento de qubits

### Flujo del Sistema

```
┌─────────────┐     I2C      ┌─────────────┐
│   Esclavo   │◄────────────►│   Maestro   │
│  (Nodo 0)   │              │   (ESP32)   │
└─────────────┘              └──────┬──────┘
                                    │ Serial
┌─────────────┐     I2C             ▼
│   Esclavo   │◄────────────►┌─────────────┐
│  (Nodo 1)   │              │  PC Client  │
└─────────────┘              │  (Python)   │
      ⋮                      └─────────────┘
```

1. El **Maestro** coordina los **Esclavos**
2. Cada Esclavo genera **4 bits** usando su LFSR con ruido
3. El **Cliente Python** recibe los 16 bits (4 esclavos × 4 bits)
4. Evalúa el **score Max-Cut** contra el grafo objetivo
5. Registra la **mejor solución** encontrada

---

## Interpretación de Resultados

### Grafo en Anillo (Demo)

En el demo incluido, usamos un **grafo en anillo** de 16 nodos:

```
       0 ─── 1 ─── 2 ─── 3
       │                 │
      15                 4
       │                 │
      14                 5
       │                 │
      13                 6
       │                 │
      12 ─── 11 ─── 10 ─── 9 ─── 8 ─── 7
```

**Score máximo teórico**: 16 (todas las aristas cortadas)

**Solución óptima**: Alternar 0-1-0-1-0-1... → `0101010101010101`

### Métricas de Salida

| Métrica | Significado |
|---------|-------------|
| **Score** | Número de aristas cortadas |
| **Eficiencia** | Score / Score_máximo × 100% |
| **Mejor tick** | Momento en que se encontró la mejor solución |
| **Configuración** | Los 16 bits que producen el mejor score |

---

## Parámetros y su Efecto

| Parámetro | Rango | Efecto |
|-----------|-------|--------|
| **T (Noise)** | 0.0 - 1.0 | Más alto = más exploración, menos estabilidad |
| **B (Bias)** | -127 a 127 | Sesgo hacia configuraciones específicas |
| **Kp (Coupling)** | 0 - 255 | Correlación entre bits vecinos |
| **M (Mode)** | 0 - 255 | Modo de operación del sampler |

### Recomendaciones

- **Exploración inicial**: T=0.5, B=0, Kp=30
- **Refinamiento**: T=0.1, B=5, Kp=60
- **Alta estabilidad**: T=0.05, B=10, Kp=100

---

## Archivos Generados

Después de cada ejecución, el script genera:

1. **`maxcut_results_YYYYMMDD_HHMMSS.csv`**
   - Todos los datos del batch
   - Columnas: tick, score, bits, is_best

2. **`maxcut_graphs_YYYYMMDD_HHMMSS.png`**
   - Evolución del mejor score vs tick
   - Histograma de distribución de scores

3. **`maxcut_graph_YYYYMMDD_HHMMSS.png`**
   - Visualización del grafo con la mejor partición
   - Nodos coloreados según su grupo

---

## Referencias

- [Max-Cut en Wikipedia](https://en.wikipedia.org/wiki/Maximum_cut)
- [Problema QUBO y Optimización Cuántica](https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization)
- Documentación oficial del proyecto Quantum32

---

**Autor**: Alejandro Rebolledo (arebolledo@udd.cl)  
**Licencia**: CC BY-NC 4.0
