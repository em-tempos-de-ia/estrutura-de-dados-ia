"""
Capítulo 10 — Estruturas Modernas e Vetoriais: Embeddings e Busca por Similaridade.

Compara a busca por similaridade do cosseno por Força Bruta (Flat Scan)
contra um índice HNSW real (biblioteca hnswlib, mesma família de algoritmo
usada por Faiss, Qdrant, Weaviate e pgvector), sobre 100.000 vetores de
128 dimensões.

Nota de metodologia: a busca é medida em lote (200 consultas), não numa
consulta isolada. Uma consulta isolada é distorcida por overhead de
chamada entre Python e a biblioteca compilada em C++, o que mascara o
ganho real do índice — o mesmo tipo de armadilha de medição discutido
no Capítulo 11.

Uso:
    python test_vector_search.py
"""
import numpy as np
import hnswlib
import time

N_VETORES = 100_000
DIMENSOES = 128
N_CONSULTAS = 200


def gerar_base(n_vetores, dimensoes, seed=42):
    rng = np.random.default_rng(seed)
    base = rng.standard_normal((n_vetores, dimensoes)).astype(np.float32)
    base /= np.linalg.norm(base, axis=1, keepdims=True)
    return base


def busca_forca_bruta(base, consultas):
    inicio = time.perf_counter()
    for q in consultas:
        similaridades = np.dot(base, q)
        np.argsort(similaridades)[-5:][::-1]
    return (time.perf_counter() - inicio) / len(consultas)


def busca_hnsw(base, consultas, n_vetores, dimensoes):
    index = hnswlib.Index(space="cosine", dim=dimensoes)
    index.init_index(max_elements=n_vetores, ef_construction=200, M=16)
    index.add_items(base, np.arange(n_vetores))
    index.set_ef(50)

    inicio = time.perf_counter()
    for q in consultas:
        index.knn_query(q, k=5)
    return (time.perf_counter() - inicio) / len(consultas)


if __name__ == "__main__":
    print(f"Gerando {N_VETORES:,} vetores com {DIMENSOES} dimensões...")
    base_vetores = gerar_base(N_VETORES, DIMENSOES)

    rng = np.random.default_rng(1)
    consultas = rng.standard_normal((N_CONSULTAS, DIMENSOES)).astype(np.float32)
    consultas /= np.linalg.norm(consultas, axis=1, keepdims=True)

    print(f"\nMedindo tempo médio por consulta ao longo de {N_CONSULTAS} consultas...")
    tempo_fb = busca_forca_bruta(base_vetores, consultas)
    tempo_hnsw = busca_hnsw(base_vetores, consultas, N_VETORES, DIMENSOES)

    print(f"\n[Força Bruta — Flat Scan O(n*d)]")
    print(f"Tempo médio por consulta: {tempo_fb * 1000:.4f} ms")

    print(f"\n[Índice HNSW real — hnswlib]")
    print(f"Tempo médio por consulta: {tempo_hnsw * 1000:.4f} ms")
    print(f"Ganho: {tempo_fb / tempo_hnsw:.1f}x mais rápido")
