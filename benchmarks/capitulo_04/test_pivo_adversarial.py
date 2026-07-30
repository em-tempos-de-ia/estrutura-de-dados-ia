"""
Capítulo 4 — Algoritmos de Ordenação.

Mede o Quick Sort com escolha de pivô ingênua (sempre o primeiro elemento)
contra dados aleatórios versus dados já ordenados (pior caso adversarial),
mostrando o colapso de O(n log n) para O(n²).

Uso:
    python test_pivo_adversarial.py
"""
import sys
import time
import random

sys.setrecursionlimit(20000)


def quicksort_pivo_ingenuo(lista):
    if len(lista) <= 1:
        return lista
    pivo = lista[0]  # sempre o primeiro elemento
    menores = [x for x in lista[1:] if x < pivo]
    maiores = [x for x in lista[1:] if x >= pivo]
    return quicksort_pivo_ingenuo(menores) + [pivo] + quicksort_pivo_ingenuo(maiores)


def executar_benchmark():
    tamanhos = [500, 1000, 2000, 4000]

    print(f"{'n':<8} | {'Dados aleatórios (s)':<22} | {'Dados já ordenados (s)':<24}")
    print("-" * 60)

    for n in tamanhos:
        aleatorios = [random.randint(0, n) for _ in range(n)]
        ja_ordenados = list(range(n))

        inicio = time.perf_counter()
        quicksort_pivo_ingenuo(aleatorios)
        t_aleatorio = time.perf_counter() - inicio

        inicio = time.perf_counter()
        quicksort_pivo_ingenuo(ja_ordenados)
        t_ordenado = time.perf_counter() - inicio

        print(f"{n:<8} | {t_aleatorio:<22.5f} | {t_ordenado:<24.5f}")


if __name__ == "__main__":
    executar_benchmark()
