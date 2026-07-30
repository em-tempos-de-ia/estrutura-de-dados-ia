"""
Capítulo 3 — Arrays, Vetores Dinâmicos e Listas Encadeadas.

Compara inserção e remoção no início da coleção: Array Dinâmico (list, O(n)
por operação) vs. Lista Duplamente Encadeada (deque, O(1) por operação).

Uso:
    python test_linear_structures.py
"""
import time
from collections import deque


def benchmark_estruturas_lineares():
    n = 100000
    dados = list(range(n))

    print(f"Iniciando teste com {n:,} elementos...\n")

    # 1. Inserção no início — Array Dinâmico (list)
    inicio = time.perf_counter()
    lista_padrao = []
    for item in dados:
        lista_padrao.insert(0, item)
    tempo_insert_list = time.perf_counter() - inicio

    # 2. Inserção no início — Lista Encadeada (deque)
    inicio = time.perf_counter()
    lista_encadeada = deque()
    for item in dados:
        lista_encadeada.appendleft(item)
    tempo_insert_deque = time.perf_counter() - inicio

    # 3. Remoção do início — Array Dinâmico (list)
    inicio = time.perf_counter()
    while len(lista_padrao) > 0:
        lista_padrao.pop(0)
    tempo_pop_list = time.perf_counter() - inicio

    # 4. Remoção do início — Lista Encadeada (deque)
    inicio = time.perf_counter()
    while len(lista_encadeada) > 0:
        lista_encadeada.popleft()
    tempo_pop_deque = time.perf_counter() - inicio

    print(f"{'Operação':<28} | {'Array Dinâmico (s)':<20} | {'Lista Encadeada (s)':<20}")
    print("-" * 74)
    print(f"{'Inserção na cabeça (0)':<28} | {tempo_insert_list:<20.5f} | {tempo_insert_deque:<20.5f}")
    print(f"{'Remoção na cabeça (0)':<28} | {tempo_pop_list:<20.5f} | {tempo_pop_deque:<20.5f}")


if __name__ == "__main__":
    benchmark_estruturas_lineares()
