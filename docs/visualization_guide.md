# Guía de Visualización: Interpretación Holográfica (Toy Model)

Este documento explica en detalle qué representan los elementos visuales en la pantalla OLED del `MasterV2` dentro del contexto de nuestra **"Simulación de Holografía de Juguete"**.

El concepto central se basa en el **Principio Holográfico** y la correspondencia **AdS/CFT** de la física teórica: la idea de que la información de un volumen de espacio (el "Bulk") está codificada completamente en su superficie exterior (el "Boundary" o Borde).

---

## 1. Barra "Bulk" (Reconstrucción del Volumen)

> **Ubicación**: Barra horizontal grande en el centro de la pantalla.
> **Valor**: Porcentaje (0% - 100%).

### ¿Qué representa?
Representa la **Integridad de la Realidad Simulada** (o la geometría del espacio-tiempo interior).
En nuestra analogía, el "Bulk" es el espacio interior donde ocurre la gravedad y la física que conocemos. Sin embargo, no tenemos acceso directo a él; debemos "reconstruirlo" matemáticamente usando solo la información que nos llega desde el borde (los Esclavos).

### Interpretación Visual
*   **100% (Barra Llena)**: **Holograma Perfecto**.
    *   La información en el borde está completa y correlacionada.
    *   Hemos logrado reconstruir todo el volumen interior sin errores.
    *   *Física*: El espacio-tiempo es suave y continuo.
*   **< 100% (Barra Parcial)**: **Pérdida de Información / Agujeros**.
    *   Partes del volumen son inaccesibles.
    *   Esto ocurre cuando los esclavos tienen demasiado ruido o están desconectados.
    *   *Física*: Es análogo a la formación de horizontes de eventos o "agujeros negros" donde la información se pierde o queda oculta para el observador externo.

---

## 2. Mapa de Borde 2x2 (Boundary Map)

> **Ubicación**: Cuadrícula de 4 celdas a la izquierda.
> **Valor**: Nivel de llenado de cada celda.

### ¿Qué representa?
Representa el **Estado del Campo en el Borde** (Boundary CFT).
Cada celda corresponde a un Esclavo físico (sensor). En la teoría holográfica, el borde es donde "viven" los datos reales (sin gravedad, solo campos cuánticos).

### Interpretación Visual
*   **Cuadro Lleno (■)**: **Baja Entropía / Alta Fidelidad**.
    *   El esclavo está funcionando perfectamente, con bajo ruido.
    *   *Física*: Estado de "baja temperatura". La información cuántica está clara y disponible para reconstruir el interior.
*   **Cuadro Vacío o Pequeño (□)**: **Alta Entropía / Ruido Térmico**.
    *   El esclavo está reportando mucho ruido (`noise` alto) o no responde.
    *   *Física*: El sistema se ha calentado. El "entrelazamiento" se ha roto o se ha vuelto caótico (scrambling), haciendo difícil o imposible usar esa parte del borde para ver el interior.

---

## 3. Gráfico de Historia (Time Evolution)

> **Ubicación**: Gráfico de líneas a la derecha.
> **Valor**: Eje Y = % de Reconstrucción, Eje X = Tiempo (últimos ~70 ticks).

### ¿Qué representa?
La **Evolución Temporal de la Estabilidad del Universo**.
Nos muestra si nuestra simulación es estable o si se está degradando con el tiempo.

### Interpretación Visual
*   **Línea Plana Arriba**: **Universo Estable**.
    *   El sistema mantiene su integridad constante. Es un estado estacionario (como un vacío estable).
*   **Fluctuaciones (Picos hacia abajo)**: **Perturbaciones**.
    *   Momentos de inestabilidad causados por ruido transitorio o desconexiones temporales.
*   **Caída Constante**: **Colapso**.
    *   Si la línea baja y se queda abajo, indica un fallo sistémico.
    *   *Física*: Podría interpretarse como la evaporación final de la información o la desconexión total del espacio-tiempo emergente.

---

## 4. Reloj (Tiempo del Observador)

> **Ubicación**: Esquina inferior derecha (HH:MM:SS).

### ¿Qué representa?
El **Tiempo Propio del Observador Externo**.
En relatividad, el tiempo es relativo. Este reloj marca el tiempo desde el marco de referencia del laboratorio (tú), que estás fuera de la "caja" del universo simulado.

---

## Resumen: ¿Cómo leer la pantalla?

1.  Miras la **Barra Central**: ¿Está al 100%? -> Todo bien.
2.  Si baja, miras el **Mapa Izquierdo**: ¿Qué esclavo (celda) está fallando (vacío)? -> Ahí está el problema.
3.  Miras el **Gráfico**: ¿Fue un error momentáneo o llevamos rato fallando?

Esta visualización transforma datos de sensores aburridos en una narrativa sobre la estabilidad de un universo de juguete.
