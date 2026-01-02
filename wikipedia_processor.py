#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
                QUANTUM32 - WIKIPEDIA DATA PROCESSOR
===============================================================================

DESCRIPCIÓN:
    Este script realiza los pasos iniciales para analizar y convertir artículos
    de Wikipedia en representaciones numéricas que puedan ser utilizadas en
    simulaciones cuánticas del sistema Quantum32.

FUNCIONALIDADES:
    1. Extracción de Artículos de Wikipedia: Usa la API wikipedia-api para
       obtener el contenido de artículos específicos.
    2. Procesamiento de Texto:
       - Limpieza de texto (eliminación de caracteres especiales, normalización)
       - Tokenización
       - Vectorización utilizando TF-IDF para convertir el texto en datos numéricos
    3. Preparación de Datos para Simulaciones Cuánticas: Organiza y exporta
       los datos vectoriales en formato compatible con otros análisis.

DEPENDENCIAS:
    - wikipedia-api (pip install wikipedia-api)
    - scikit-learn (pip install scikit-learn)
    - pandas (pip install pandas)
    - numpy (instalado con scikit-learn)

OUTPUTS:
    - CSV: Archivo con vectores TF-IDF de artículos procesados
    - JSON: Metadata de los artículos procesados
    - NPY: Matrices numpy para fácil carga en simulaciones

EJEMPLO DE USO:
    # Modo interactivo
    python wikipedia_processor.py

    # Modo programático
    from wikipedia_processor import WikipediaProcessor
    processor = WikipediaProcessor(language='es')
    data = processor.process_articles(['Mecánica cuántica', 'Computación cuántica'])
    processor.export_data(data, 'quantum_articles')

AUTOR: Basado en el estilo de Quantum32 Hybrid Sampler
LICENCIA: CC BY-NC 4.0
===============================================================================
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

try:
    import wikipediaapi
    WIKIPEDIA_OK = True
except ImportError:
    WIKIPEDIA_OK = False
    print("ERROR: wikipedia-api no está instalada.")
    print("Instalar con: pip install wikipedia-api")

try:
    import pandas as pd
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False
    print("ERROR: pandas no está instalado.")
    print("Instalar con: pip install pandas")

try:
    import numpy as np
    NUMPY_OK = True
except ImportError:
    NUMPY_OK = False
    print("ERROR: numpy no está instalado.")
    print("Instalar con: pip install numpy")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize
    SKLEARN_OK = True
except ImportError:
    SKLEARN_OK = False
    print("ERROR: scikit-learn no está instalado.")
    print("Instalar con: pip install scikit-learn")


# -------------------------
# CONFIGURACIÓN POR DEFECTO
# -------------------------
DEFAULT_LANGUAGE = 'es'
DEFAULT_USER_AGENT = 'Quantum32WikiProcessor/1.0 (https://github.com/vlorcap1/Quantum32)'
DEFAULT_MAX_FEATURES = 100  # Número de características TF-IDF a extraer
DEFAULT_OUTPUT_DIR = 'wikipedia_data'


class WikipediaProcessor:
    """
    Procesador de artículos de Wikipedia para preparar datos para simulaciones
    cuánticas en el sistema Quantum32.
    """

    def __init__(
        self,
        language: str = DEFAULT_LANGUAGE,
        user_agent: str = DEFAULT_USER_AGENT,
        max_features: int = DEFAULT_MAX_FEATURES,
        output_dir: str = DEFAULT_OUTPUT_DIR
    ):
        """
        Inicializa el procesador de Wikipedia.

        Args:
            language: Código de idioma de Wikipedia (ej: 'es', 'en')
            user_agent: User agent para las peticiones a la API
            max_features: Número máximo de características TF-IDF
            output_dir: Directorio para guardar los datos procesados
        """
        if not all([WIKIPEDIA_OK, PANDAS_OK, NUMPY_OK, SKLEARN_OK]):
            raise RuntimeError(
                "Faltan dependencias requeridas. Ejecuta:\n"
                "pip install wikipedia-api scikit-learn pandas"
            )

        self.language = language
        self.user_agent = user_agent
        self.max_features = max_features
        self.output_dir = output_dir

        # Inicializar API de Wikipedia
        self.wiki = wikipediaapi.Wikipedia(
            user_agent=user_agent,
            language=language
        )

        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)

        print(f"WikipediaProcessor inicializado:")
        print(f"  - Idioma: {language}")
        print(f"  - Max features: {max_features}")
        print(f"  - Output dir: {output_dir}")

    def clean_text(self, text: str) -> str:
        """
        Limpia el texto eliminando caracteres especiales y normalizando.

        Args:
            text: Texto a limpiar

        Returns:
            Texto limpio
        """
        # Convertir a minúsculas
        text = text.lower()

        # Eliminar URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)

        # Eliminar referencias [1], [2], [1-3], etc.
        text = re.sub(r'\[\d+(?:-\d+)?\]', '', text)

        # Eliminar caracteres especiales pero mantener espacios y puntuación básica
        text = re.sub(r'[^\w\s\.\,\;\:\-]', ' ', text)

        # Normalizar espacios múltiples
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def fetch_article(self, title: str, summary_length: int = 500) -> Optional[Dict[str, Any]]:
        """
        Obtiene un artículo de Wikipedia.

        Args:
            title: Título del artículo

        Returns:
            Diccionario con información del artículo o None si no existe
        """
        print(f"Obteniendo artículo: '{title}'...")

        page = self.wiki.page(title)

        if not page.exists():
            print(f"  ⚠ Artículo '{title}' no encontrado")
            return None

        # Extraer información
        article = {
            'title': page.title,
            'url': page.fullurl,
            'summary': page.summary[:summary_length] if page.summary else '',  # Configurable length
            'text': page.text,
            'categories': list(page.categories.keys())[:10],  # Primeras 10 categorías
            'links_count': len(page.links),
            'length': len(page.text),
            'fetched_at': datetime.now().isoformat()
        }

        print(f"  ✓ Artículo obtenido: {len(article['text'])} caracteres")
        return article

    def fetch_articles(self, titles: List[str]) -> List[Dict[str, Any]]:
        """
        Obtiene múltiples artículos de Wikipedia.

        Args:
            titles: Lista de títulos de artículos

        Returns:
            Lista de diccionarios con información de los artículos
        """
        articles = []

        for title in titles:
            article = self.fetch_article(title)
            if article:
                articles.append(article)

        print(f"\n{len(articles)}/{len(titles)} artículos obtenidos exitosamente")
        return articles

    def tokenize_and_vectorize(
        self,
        articles: List[Dict[str, Any]]
    ) -> Tuple[np.ndarray, List[str], Dict[str, Any]]:
        """
        Tokeniza y vectoriza los artículos usando TF-IDF.

        Args:
            articles: Lista de artículos obtenidos

        Returns:
            Tupla con (matriz TF-IDF, lista de features, metadata)
        """
        if not articles:
            raise ValueError("No hay artículos para procesar")

        print("\nProcesando texto...")

        # Limpiar textos
        texts = [self.clean_text(article['text']) for article in articles]
        titles = [article['title'] for article in articles]

        print(f"  - {len(texts)} textos limpiados")

        # Vectorización TF-IDF
        print(f"  - Vectorizando con TF-IDF (max_features={self.max_features})...")

        # Configure stop words based on language
        stop_words_config = None
        if self.language in ['en', 'english']:
            stop_words_config = 'english'
        # Note: scikit-learn has limited language support for stop words
        # For Spanish and other languages, consider using external libraries

        vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            stop_words=stop_words_config,
            ngram_range=(1, 2),  # Unigramas y bigramas
            min_df=1,
            max_df=0.95
        )

        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()

        print(f"  ✓ Matriz TF-IDF creada: {tfidf_matrix.shape}")
        print(f"  ✓ Features extraídos: {len(feature_names)}")

        # Normalizar vectores (útil para simulaciones cuánticas)
        tfidf_normalized = normalize(tfidf_matrix, norm='l2')

        # Metadata
        metadata = {
            'n_articles': len(articles),
            'n_features': len(feature_names),
            'feature_names': feature_names.tolist(),
            'article_titles': titles,
            'vectorizer_params': {
                'max_features': self.max_features,
                'ngram_range': (1, 2)
            },
            'processed_at': datetime.now().isoformat()
        }

        return tfidf_normalized.toarray(), feature_names.tolist(), metadata

    def process_articles(
        self,
        titles: List[str]
    ) -> Dict[str, Any]:
        """
        Pipeline completo: obtiene, limpia, tokeniza y vectoriza artículos.

        Args:
            titles: Lista de títulos de artículos de Wikipedia

        Returns:
            Diccionario con todos los datos procesados
        """
        print("="*70)
        print("         PROCESAMIENTO DE ARTÍCULOS DE WIKIPEDIA")
        print("="*70)

        # Obtener artículos
        articles = self.fetch_articles(titles)

        if not articles:
            print("\n⚠ No se obtuvieron artículos. Abortando.")
            return {
                'articles': [],
                'tfidf_matrix': None,
                'feature_names': [],
                'metadata': {'n_articles': 0, 'n_features': 0}
            }

        # Vectorizar
        tfidf_matrix, feature_names, metadata = self.tokenize_and_vectorize(articles)

        # Preparar resultado
        result = {
            'articles': articles,
            'tfidf_matrix': tfidf_matrix,
            'feature_names': feature_names,
            'metadata': metadata
        }

        print("\n" + "="*70)
        print("                     PROCESAMIENTO COMPLETO")
        print("="*70)

        return result

    def export_data(
        self,
        data: Dict[str, Any],
        base_filename: str = 'wikipedia_processed'
    ) -> Dict[str, str]:
        """
        Exporta los datos procesados en múltiples formatos.

        Args:
            data: Datos procesados del método process_articles
            base_filename: Nombre base para los archivos de salida

        Returns:
            Diccionario con rutas de archivos generados
        """
        if not data:
            print("No hay datos para exportar")
            return {}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_path = os.path.join(self.output_dir, f"{base_filename}_{timestamp}")

        exported_files = {}

        print("\nExportando datos...")

        # 1. Matriz TF-IDF como numpy array (formato binario eficiente)
        npy_path = f"{base_path}_tfidf.npy"
        np.save(npy_path, data['tfidf_matrix'])
        exported_files['tfidf_matrix'] = npy_path
        print(f"  ✓ Matriz TF-IDF: {npy_path}")

        # 2. CSV con features (para análisis en Excel/Python)
        csv_path = f"{base_path}_features.csv"
        df = pd.DataFrame(
            data['tfidf_matrix'],
            columns=data['feature_names'],
            index=data['metadata']['article_titles']
        )
        df.to_csv(csv_path, encoding='utf-8')
        exported_files['features_csv'] = csv_path
        print(f"  ✓ Features CSV: {csv_path}")

        # 3. Metadata JSON
        json_path = f"{base_path}_metadata.json"
        metadata_export = data['metadata'].copy()
        # Remover feature_names del JSON (ya están en CSV) para reducir tamaño
        if 'feature_names' in metadata_export:
            metadata_export['feature_names_count'] = len(metadata_export['feature_names'])
            metadata_export.pop('feature_names')

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_export, f, indent=2, ensure_ascii=False)
        exported_files['metadata'] = json_path
        print(f"  ✓ Metadata JSON: {json_path}")

        # 4. Artículos completos JSON (para referencia)
        articles_json_path = f"{base_path}_articles.json"
        articles_export = [
            {
                'title': a['title'],
                'url': a['url'],
                'summary': a['summary'],
                'categories': a['categories'],
                'length': a['length'],
                'links_count': a['links_count'],
                'fetched_at': a['fetched_at']
            }
            for a in data['articles']
        ]

        with open(articles_json_path, 'w', encoding='utf-8') as f:
            json.dump(articles_export, f, indent=2, ensure_ascii=False)
        exported_files['articles'] = articles_json_path
        print(f"  ✓ Artículos JSON: {articles_json_path}")

        # 5. Feature names (lista de términos importantes)
        features_txt_path = f"{base_path}_feature_names.txt"
        with open(features_txt_path, 'w', encoding='utf-8') as f:
            for i, feature in enumerate(data['feature_names'], 1):
                f.write(f"{i}. {feature}\n")
        exported_files['feature_names'] = features_txt_path
        print(f"  ✓ Feature names: {features_txt_path}")

        print(f"\n✓ Datos exportados exitosamente en: {self.output_dir}/")

        return exported_files

    def get_top_features_per_article(
        self,
        data: Dict[str, Any],
        top_n: int = 10
    ) -> Dict[str, List[Tuple[str, float]]]:
        """
        Obtiene los términos más importantes para cada artículo.

        Args:
            data: Datos procesados
            top_n: Número de términos top a retornar

        Returns:
            Diccionario con título del artículo y sus top términos
        """
        result = {}

        for i, title in enumerate(data['metadata']['article_titles']):
            # Obtener scores TF-IDF para este artículo
            scores = data['tfidf_matrix'][i]

            # Obtener índices de los top N scores
            top_indices = np.argsort(scores)[-top_n:][::-1]

            # Obtener términos y scores
            top_terms = [
                (data['feature_names'][idx], scores[idx])
                for idx in top_indices
                if scores[idx] > 0
            ]

            result[title] = top_terms

        return result


# -------------------------
# FUNCIONES AUXILIARES
# -------------------------
def print_analysis(data: Dict[str, Any]):
    """
    Imprime un análisis resumido de los datos procesados.
    """
    print("\n" + "="*70)
    print("                        ANÁLISIS DE DATOS")
    print("="*70)

    metadata = data['metadata']
    print(f"\nArtículos procesados: {metadata['n_articles']}")
    print(f"Features extraídos: {metadata['n_features']}")
    print(f"Dimensión de matriz: {data['tfidf_matrix'].shape}")

    print("\nArtículos:")
    for i, title in enumerate(metadata['article_titles'], 1):
        print(f"  {i}. {title}")

    # Estadísticas de la matriz
    print("\nEstadísticas de vectorización:")
    print(f"  - Valores no-cero: {np.count_nonzero(data['tfidf_matrix'])}")
    print(f"  - Sparsity: {100 * (1 - np.count_nonzero(data['tfidf_matrix']) / data['tfidf_matrix'].size):.2f}%")
    print(f"  - Media de scores: {np.mean(data['tfidf_matrix']):.4f}")
    print(f"  - Std de scores: {np.std(data['tfidf_matrix']):.4f}")

    # Top features globales
    print("\nTop 10 features globales (por suma de TF-IDF):")
    global_scores = np.sum(data['tfidf_matrix'], axis=0)
    top_global_indices = np.argsort(global_scores)[-10:][::-1]

    for i, idx in enumerate(top_global_indices, 1):
        feature = data['feature_names'][idx]
        score = global_scores[idx]
        print(f"  {i}. {feature}: {score:.4f}")


def safe_input(prompt: str, default: Any) -> str:
    """
    Input seguro que retorna el default si hay error.
    """
    try:
        value = input(f"{prompt} [{default}]: ").strip()
        return value if value else str(default)
    except (EOFError, KeyboardInterrupt):
        return str(default)
    except Exception:
        return str(default)


# -------------------------
# MAIN - MODO INTERACTIVO
# -------------------------
def main():
    """
    Función principal para modo interactivo.
    """
    print("="*70)
    print("       QUANTUM32 - PROCESADOR DE ARTÍCULOS DE WIKIPEDIA")
    print("="*70)

    if not all([WIKIPEDIA_OK, PANDAS_OK, NUMPY_OK, SKLEARN_OK]):
        print("\n⚠ Faltan dependencias. Instala con:")
        print("pip install wikipedia-api scikit-learn pandas")
        return

    # Solicitar configuración
    print("\n--- CONFIGURACIÓN ---")
    language = safe_input("Idioma de Wikipedia (es/en)", DEFAULT_LANGUAGE)
    
    try:
        max_features = int(safe_input("Máximo de features TF-IDF", DEFAULT_MAX_FEATURES))
    except ValueError:
        print(f"  ⚠ Valor inválido, usando default: {DEFAULT_MAX_FEATURES}")
        max_features = DEFAULT_MAX_FEATURES

    # Solicitar artículos
    print("\n--- ARTÍCULOS A PROCESAR ---")
    print("Ingresa los títulos de los artículos (uno por línea).")
    print("Deja una línea en blanco para terminar.")
    print("Ejemplo: 'Mecánica cuántica', 'Computación cuántica', etc.\n")

    titles = []
    while True:
        try:
            title = input(f"Artículo {len(titles) + 1}: ").strip()
            if not title:
                break
            titles.append(title)
        except (EOFError, KeyboardInterrupt):
            break

    if not titles:
        print("\n⚠ No se ingresaron artículos. Usando ejemplos por defecto...")
        titles = ['Mecánica cuántica', 'Computación cuántica', 'Física cuántica']

    print(f"\nArtículos a procesar: {len(titles)}")

    # Crear procesador
    processor = WikipediaProcessor(
        language=language,
        max_features=max_features
    )

    # Procesar artículos
    data = processor.process_articles(titles)

    if not data:
        print("\n⚠ No se pudieron procesar artículos.")
        return

    # Mostrar análisis
    print_analysis(data)

    # Exportar datos
    print("\n--- EXPORTACIÓN ---")
    export = safe_input("¿Exportar datos? (s/n)", "s").lower()

    if export in ['s', 'y', 'yes', 'si', 'sí']:
        exported_files = processor.export_data(data)

        # Mostrar top features por artículo
        print("\n--- TOP FEATURES POR ARTÍCULO ---")
        top_features = processor.get_top_features_per_article(data, top_n=5)

        for title, features in top_features.items():
            print(f"\n{title}:")
            for i, (term, score) in enumerate(features, 1):
                print(f"  {i}. {term}: {score:.4f}")

    print("\n" + "="*70)
    print("                    ¡PROCESAMIENTO COMPLETO!")
    print("="*70)
    print("\nLos datos están listos para ser utilizados en simulaciones Quantum32.")
    print("Para cargar los datos en otro script Python:")
    print("  import numpy as np")
    print("  tfidf_matrix = np.load('wikipedia_data/<archivo>_tfidf.npy')")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n⚠ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
