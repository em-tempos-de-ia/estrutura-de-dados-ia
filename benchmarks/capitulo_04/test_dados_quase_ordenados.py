"""
Capítulo 4 — Algoritmos de Ordenação.

Compara Merge Sort puro (sempre O(n log n), não-adaptativo) contra o sort()
nativo do Python (Timsort/Powersort, adaptativo) em dados quase ordenados,
evidenciando a vantagem prática do algoritmo que explora ordem pré-existente.

Uso:
    python test_dados_quase_ordenados.py
"""
import time
import random


def merge_sort(lista):
    if len(lista) <= 1:
        return lista
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])
    return _merge(esquerda, direita)


def _merge(esquerda, direita):
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


def gerar_quase_ordenado(n, perturbacoes=None):
    """Lista 0..n-1 com um pequeno número de trocas aleatórias."""
    if perturbacoes is None:
        perturbacoes = max(1, n // 100)  # ~1% de desordem
    dados = list(range(n))
    for _ in range(perturbacoes):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        dados[i], dados[j] = dados[j], dados[i]
    return dados


def executar_benchmark():
    tamanhos = [2000, 4000, 8000, 16000]

    print(f"{'n':<8} | {'Merge Sort puro (s)':<20} | {'sorted() nativo (s)':<20} | {'Vantagem do nativo':<18}")
    print("-" * 72)

    for n in tamanhos:
        dados = gerar_quase_ordenado(n)

        inicio = time.perf_counter()
        merge_sort(dados)
        t_merge = time.perf_counter() - inicio

        inicio = time.perf_counter()
        sorted(dados)
        t_nativo = time.perf_counter() - inicio

        vantagem = f"{t_merge / t_nativo:.1f}x" if t_nativo > 0 else "n/a"
        print(f"{n:<8} | {t_merge:<20.5f} | {t_nativo:<20.5f} | {vantagem:<18}")


if __name__ == "__main__":
    executar_benchmark()
