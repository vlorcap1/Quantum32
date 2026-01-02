#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
                EJEMPLO DE USO - WIKIPEDIA PROCESSOR
===============================================================================

Este script demuestra el uso básico del procesador de Wikipedia para
preparar datos para simulaciones Quantum32.

Ejecuta este script para ver el procesador en acción:
    python ejemplo_uso.py

===============================================================================
"""

from wikipedia_processor import WikipediaProcessor


def ejemplo_simple():
    """
    Ejemplo simple: procesar unos pocos artículos de física cuántica.
    """
    print("\n" + "="*70)
    print("       EJEMPLO: Procesamiento de Artículos de Física Cuántica")
    print("="*70)
    
    # 1. Crear el procesador
    processor = WikipediaProcessor(
        language='es',           # Idioma español
        max_features=50,         # Extraer 50 términos principales
        output_dir='ejemplos'    # Guardar en carpeta 'ejemplos'
    )
    
    # 2. Definir artículos a procesar
    articulos = [
        'Mecánica cuántica',
        'Computación cuántica',
        'Qubit'
    ]
    
    print(f"\nArtículos a procesar: {articulos}")
    
    # 3. Procesar artículos (extrae, limpia, vectoriza)
    print("\nProcesando...")
    data = processor.process_articles(articulos)
    
    if not data:
        print("\n⚠ No se pudieron obtener artículos (verifica conexión a internet)")
        return
    
    # 4. Mostrar información básica
    print("\n--- RESULTADOS ---")
    print(f"Artículos procesados: {data['metadata']['n_articles']}")
    print(f"Features extraídos: {data['metadata']['n_features']}")
    print(f"Dimensión de matriz TF-IDF: {data['tfidf_matrix'].shape}")
    
    # 5. Mostrar top términos por artículo
    print("\n--- TOP 5 TÉRMINOS POR ARTÍCULO ---")
    top_features = processor.get_top_features_per_article(data, top_n=5)
    
    for titulo, terminos in top_features.items():
        print(f"\n{titulo}:")
        for i, (termino, score) in enumerate(terminos, 1):
            print(f"  {i}. {termino}: {score:.4f}")
    
    # 6. Exportar datos
    print("\n--- EXPORTANDO DATOS ---")
    archivos = processor.export_data(data, base_filename='ejemplo_quantum')
    
    print("\n✓ Ejemplo completado exitosamente!")
    print(f"\nLos datos están guardados en la carpeta: {processor.output_dir}/")
    print("\nPuedes cargar estos datos en tus simulaciones con:")
    print("  import numpy as np")
    print(f"  matriz = np.load('{archivos['tfidf_matrix']}')")


def ejemplo_analisis_similitud():
    """
    Ejemplo avanzado: calcular similitud entre artículos.
    """
    print("\n\n" + "="*70)
    print("       EJEMPLO: Análisis de Similitud entre Artículos")
    print("="*70)
    
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    
    processor = WikipediaProcessor(language='es', max_features=100)
    
    # Artículos relacionados y uno menos relacionado
    articulos = [
        'Mecánica cuántica',
        'Física cuántica',
        'Astronomía'  # Menos relacionado con cuántica
    ]
    
    print(f"\nArtículos: {articulos}")
    print("\nProcesando...")
    
    data = processor.process_articles(articulos)
    
    if not data:
        print("\n⚠ No se pudieron obtener artículos")
        return
    
    # Calcular matriz de similitud
    similitud = cosine_similarity(data['tfidf_matrix'])
    
    print("\n--- MATRIZ DE SIMILITUD (Coseno) ---")
    print("\nValores entre 0 (diferentes) y 1 (idénticos):\n")
    
    # Imprimir matriz formateada
    print(f"{'':25}", end='')
    for titulo in articulos:
        print(f"{titulo[:20]:20}", end='')
    print()
    
    for i, titulo_i in enumerate(articulos):
        print(f"{titulo_i[:25]:25}", end='')
        for j, titulo_j in enumerate(articulos):
            print(f"{similitud[i][j]:20.4f}", end='')
        print()
    
    # Interpretación
    print("\n--- INTERPRETACIÓN ---")
    max_sim = 0
    max_pair = None
    
    for i in range(len(articulos)):
        for j in range(i+1, len(articulos)):
            if similitud[i][j] > max_sim:
                max_sim = similitud[i][j]
                max_pair = (articulos[i], articulos[j])
    
    if max_pair:
        print(f"\nPar más similar: '{max_pair[0]}' y '{max_pair[1]}'")
        print(f"Similitud: {max_sim:.4f}")


def ejemplo_quantum_encoding():
    """
    Ejemplo: convertir vectores TF-IDF a bits para qubits.
    """
    print("\n\n" + "="*70)
    print("       EJEMPLO: Encoding Cuántico - Vector a Bits")
    print("="*70)
    
    import numpy as np
    
    processor = WikipediaProcessor(language='es', max_features=16)
    
    articulos = ['Qubit', 'Superposición cuántica']
    
    print(f"\nArtículos: {articulos}")
    print("\nProcesando...")
    
    data = processor.process_articles(articulos)
    
    if not data:
        print("\n⚠ No se pudieron obtener artículos")
        return
    
    print("\n--- CONVERSIÓN A REPRESENTACIÓN BINARIA ---")
    print("(Útil para mapear a qubits en simulaciones)\n")
    
    for i, titulo in enumerate(articulos):
        vector = data['tfidf_matrix'][i]
        
        # Convertir a binario usando mediana como threshold
        threshold = np.median(vector[vector > 0])
        vector_binario = (vector > threshold).astype(int)
        
        bitstring = ''.join(map(str, vector_binario))
        
        print(f"{titulo}:")
        print(f"  Vector continuo (primeros 10): {vector[:10]}")
        print(f"  Threshold: {threshold:.4f}")
        print(f"  Vector binario: {bitstring}")
        print(f"  Número de 1s: {np.sum(vector_binario)}/{len(vector_binario)}")
        print()


def main():
    """
    Ejecuta todos los ejemplos.
    """
    print("#"*70)
    print("#" + " "*68 + "#")
    print("#" + " "*15 + "EJEMPLOS DE WIKIPEDIA PROCESSOR" + " "*22 + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    try:
        # Ejemplo 1: Uso básico
        ejemplo_simple()
        
        # Ejemplo 2: Análisis de similitud
        ejemplo_analisis_similitud()
        
        # Ejemplo 3: Encoding cuántico
        ejemplo_quantum_encoding()
        
        print("\n" + "="*70)
        print("                  ¡TODOS LOS EJEMPLOS COMPLETADOS!")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Interrumpido por el usuario.")
    except Exception as e:
        print(f"\n⚠ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
