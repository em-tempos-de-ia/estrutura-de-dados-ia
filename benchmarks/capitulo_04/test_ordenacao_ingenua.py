"""
Capítulo 4 — Algoritmos de Ordenação.

Compara a família O(n²) (Bolha, Inserção) contra o sort() nativo do Python
(Timsort/Powersort, O(n log n)), em n crescente, sobre dados aleatórios.

Uso:
    python test_ordenacao_ingenua.py
"""
import time
import random


def bolha(lista):
    a = lista[:]
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def insercao(lista):
    a = lista[:]
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        while j >= 0 and a[j] > chave:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = chave
    return a


def executar_benchmark():
    tamanhos = [500, 1000, 2000, 4000, 8000]

    print(f"{'n':<8} | {'Bolha O(n²) (s)':<18} | {'Inserção O(n²) (s)':<20} | {'sorted() nativo (s)':<20}")
    print("-" * 72)

    for n in tamanhos:
        dados = [random.randint(0, n) for _ in range(n)]

        inicio = time.perf_counter()
        bolha(dados)
        t_bolha = time.perf_counter() - inicio

        inicio = time.perf_counter()
        insercao(dados)
        t_insercao = time.perf_counter() - inicio

        inicio = time.perf_counter()
        sorted(dados)
        t_nativo = time.perf_counter() - inicio

        print(f"{n:<8} | {t_bolha:<18.5f} | {t_insercao:<20.5f} | {t_nativo:<20.5f}")


if __name__ == "__main__":
    executar_benchmark()
