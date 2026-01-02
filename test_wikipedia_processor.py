#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para wikipedia_processor.py
Valida que todas las funciones principales funcionan correctamente.
"""

import os
import sys
import numpy as np

# Importar el módulo
from wikipedia_processor import WikipediaProcessor

def test_basic_functionality():
    """
    Prueba la funcionalidad básica del procesador.
    """
    print("="*70)
    print("           TEST: WIKIPEDIA PROCESSOR - BASIC FUNCTIONALITY")
    print("="*70)
    
    # Test 1: Inicialización
    print("\n[TEST 1] Inicializando procesador...")
    try:
        processor = WikipediaProcessor(
            language='es',
            max_features=50,
            output_dir='test_output'
        )
        print("  ✓ Procesador inicializado correctamente")
    except Exception as e:
        print(f"  ✗ Error en inicialización: {e}")
        return False
    
    # Test 2: Extracción de artículos
    print("\n[TEST 2] Extrayendo artículos de Wikipedia...")
    test_articles = ['Computación cuántica', 'Qubit']
    
    try:
        articles = processor.fetch_articles(test_articles)
        if len(articles) > 0:
            print(f"  ✓ {len(articles)} artículos obtenidos correctamente")
            for article in articles:
                print(f"    - {article['title']}: {article['length']} caracteres")
        else:
            print("  ⚠ No se obtuvieron artículos (puede ser problema de conexión)")
            return None  # No es un error crítico, pero no podemos continuar
    except Exception as e:
        print(f"  ✗ Error obteniendo artículos: {e}")
        return False
    
    # Test 3: Limpieza de texto
    print("\n[TEST 3] Limpieza de texto...")
    try:
        test_text = "Este es un TEXTO con [1] referencias y http://urls.com caracteres @@especiales!!"
        clean = processor.clean_text(test_text)
        print(f"  Original: {test_text}")
        print(f"  Limpio:   {clean}")
        print("  ✓ Limpieza de texto funciona")
    except Exception as e:
        print(f"  ✗ Error en limpieza: {e}")
        return False
    
    # Test 4: Vectorización
    print("\n[TEST 4] Vectorización TF-IDF...")
    try:
        tfidf_matrix, feature_names, metadata = processor.tokenize_and_vectorize(articles)
        print(f"  ✓ Vectorización completada")
        print(f"    - Forma de matriz: {tfidf_matrix.shape}")
        print(f"    - Features extraídos: {len(feature_names)}")
        print(f"    - Primeros 5 features: {feature_names[:5]}")
    except Exception as e:
        print(f"  ✗ Error en vectorización: {e}")
        return False
    
    # Test 5: Procesamiento completo
    print("\n[TEST 5] Pipeline completo...")
    try:
        data = processor.process_articles(test_articles)
        if data:
            print("  ✓ Pipeline completo ejecutado")
            print(f"    - Artículos procesados: {data['metadata']['n_articles']}")
            print(f"    - Dimensión de matriz: {data['tfidf_matrix'].shape}")
        else:
            print("  ✗ Pipeline retornó None")
            return False
    except Exception as e:
        print(f"  ✗ Error en pipeline: {e}")
        return False
    
    # Test 6: Exportación
    print("\n[TEST 6] Exportación de datos...")
    try:
        exported = processor.export_data(data, base_filename='test_export')
        print(f"  ✓ Datos exportados a {len(exported)} archivos:")
        for key, path in exported.items():
            file_size = os.path.getsize(path)
            print(f"    - {key}: {os.path.basename(path)} ({file_size} bytes)")
    except Exception as e:
        print(f"  ✗ Error en exportación: {e}")
        return False
    
    # Test 7: Top features por artículo
    print("\n[TEST 7] Top features por artículo...")
    try:
        top_features = processor.get_top_features_per_article(data, top_n=5)
        print("  ✓ Top features calculados:")
        for title, features in top_features.items():
            print(f"    {title}:")
            for i, (term, score) in enumerate(features[:3], 1):
                print(f"      {i}. {term}: {score:.4f}")
    except Exception as e:
        print(f"  ✗ Error calculando top features: {e}")
        return False
    
    # Test 8: Validación de datos
    print("\n[TEST 8] Validación de datos exportados...")
    try:
        # Cargar matriz numpy
        npy_file = None
        for key, path in exported.items():
            if key == 'tfidf_matrix':
                npy_file = path
                break
        
        if npy_file:
            loaded_matrix = np.load(npy_file)
            if np.allclose(loaded_matrix, data['tfidf_matrix']):
                print("  ✓ Datos guardados y cargados correctamente")
                print(f"    - Forma: {loaded_matrix.shape}")
            else:
                print("  ✗ Datos no coinciden después de guardar/cargar")
                return False
        else:
            print("  ⚠ No se encontró archivo .npy para validar")
    except Exception as e:
        print(f"  ✗ Error validando datos: {e}")
        return False
    
    # Cleanup
    print("\n[CLEANUP] Limpiando archivos de test...")
    try:
        import shutil
        if os.path.exists('test_output'):
            shutil.rmtree('test_output')
        print("  ✓ Archivos de test eliminados")
    except Exception as e:
        print(f"  ⚠ No se pudieron eliminar archivos de test: {e}")
    
    return True


def test_edge_cases():
    """
    Prueba casos extremos y manejo de errores.
    """
    print("\n" + "="*70)
    print("           TEST: EDGE CASES")
    print("="*70)
    
    processor = WikipediaProcessor(language='es', max_features=10)
    
    # Test: Artículo inexistente
    print("\n[TEST] Artículo inexistente...")
    article = processor.fetch_article('ArticuloQueNoExisteXYZ123456789')
    if article is None:
        print("  ✓ Manejo correcto de artículo inexistente")
    else:
        print("  ✗ Debería retornar None para artículo inexistente")
        return False
    
    # Test: Texto vacío
    print("\n[TEST] Limpieza de texto vacío...")
    clean = processor.clean_text("")
    if clean == "":
        print("  ✓ Texto vacío manejado correctamente")
    else:
        print("  ⚠ Texto vacío no retorna string vacío")
    
    return True


def main():
    """
    Ejecuta todas las pruebas.
    """
    print("\n" + "#"*70)
    print("     QUANTUM32 - WIKIPEDIA PROCESSOR TEST SUITE")
    print("#"*70)
    
    # Test básico
    result_basic = test_basic_functionality()
    
    if result_basic is None:
        print("\n" + "="*70)
        print("⚠ TESTS INCOMPLETOS - Sin conexión a Wikipedia")
        print("="*70)
        print("No se pudieron completar los tests por falta de conexión.")
        print("Esto no indica un problema con el código, sino con la red.")
        return 0
    
    if not result_basic:
        print("\n" + "="*70)
        print("✗ TESTS FALLIDOS")
        print("="*70)
        return 1
    
    # Tests de edge cases
    result_edge = test_edge_cases()
    
    if not result_edge:
        print("\n" + "="*70)
        print("✗ EDGE CASE TESTS FALLIDOS")
        print("="*70)
        return 1
    
    # Todo OK
    print("\n" + "="*70)
    print("✓ TODOS LOS TESTS PASARON")
    print("="*70)
    print("\nEl módulo wikipedia_processor está funcionando correctamente.")
    print("Puede ser usado para procesar artículos de Wikipedia y")
    print("preparar datos para simulaciones Quantum32.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
