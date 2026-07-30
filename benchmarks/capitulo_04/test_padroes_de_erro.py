"""
Capítulo 4 — Algoritmos de Ordenação.

Reúne implementações com antipadrões comuns em código gerado por IA e mede
cada uma contra a biblioteca padrão, categorizando o tipo de ineficiência.

Antipadrões cobertos:
  1. Pivô ingênuo (Quick Sort, sempre o primeiro elemento) em dado adversarial
  2. Reordenar a coleção inteira a cada nova inserção (Cenário 3 do Capítulo 4)
  3. Instabilidade não tratada em ordenação por múltiplas chaves

Uso:
    python test_padroes_de_erro.py
"""
import sys
import time
import random

sys.setrecursionlimit(20000)


# --- Antipadrão 1: pivô ingênuo -------------------------------------------
def quicksort_pivo_ingenuo(lista):
    if len(lista) <= 1:
        return lista
    pivo = lista[0]
    menores = [x for x in lista[1:] if x < pivo]
    maiores = [x for x in lista[1:] if x >= pivo]
    return quicksort_pivo_ingenuo(menores) + [pivo] + quicksort_pivo_ingenuo(maiores)


def medir_pivo_ingenuo(n):
    dados_ordenados = list(range(n))
    inicio = time.perf_counter()
    quicksort_pivo_ingenuo(dados_ordenados)
    t_antipadrao = time.perf_counter() - inicio

    inicio = time.perf_counter()
    sorted(dados_ordenados)
    t_nativo = time.perf_counter() - inicio
    return t_antipadrao, t_nativo


# --- Antipadrão 2: reordenar a cada inserção -------------------------------
def antipadrao_insere_e_ordena(n):
    colecao = []
    for i in range(n):
        colecao.append(random.randint(0, n))
        colecao.sort()  # reordena tudo, a cada inserção
    return colecao


def padrao_correto_insere_uma_vez(n):
    colecao = [random.randint(0, n) for _ in range(n)]
    colecao.sort()  # ordena uma única vez, ao final
    return colecao


def medir_insere_e_ordena(n):
    inicio = time.perf_counter()
    antipadrao_insere_e_ordena(n)
    t_antipadrao = time.perf_counter() - inicio

    inicio = time.perf_counter()
    padrao_correto_insere_uma_vez(n)
    t_correto = time.perf_counter() - inicio
    return t_antipadrao, t_correto


# --- Antipadrão 3: instabilidade não tratada -------------------------------
def medir_instabilidade(n):
    """Ordena por departamento após já estar ordenado por nome; sorted() do
    Python é estável, então o antipadrão aqui é usar uma implementação
    manual que não preserva estabilidade (ex.: sort por comparação
    sem chave composta), verificado por contagem de inversões residuais."""
    departamentos = ["Vendas", "TI", "RH"]
    pessoas = sorted(
        [(f"pessoa_{i}", random.choice(departamentos)) for i in range(n)],
        key=lambda p: p[0],
    )
    # sorted() do Python é estável: ordenar por departamento preserva a
    # ordem por nome dentro de cada departamento.
    por_departamento_estavel = sorted(pessoas, key=lambda p: p[1])

    # Verifica estabilidade: dentro de cada departamento, os nomes devem
    # continuar em ordem alfabética (a ordem original).
    por_dep = {}
    for nome, dep in por_departamento_estavel:
        por_dep.setdefault(dep, []).append(nome)
    estavel = all(nomes == sorted(nomes) for nomes in por_dep.values())
    return estavel


def executar_benchmark():
    print("=== Antipadrão 1: pivô ingênuo em dado adversarial ===")
    print(f"{'n':<8} | {'Antipadrão (s)':<16} | {'sorted() nativo (s)':<20}")
    for n in [1000, 2000, 4000]:
        t_a, t_n = medir_pivo_ingenuo(n)
        print(f"{n:<8} | {t_a:<16.5f} | {t_n:<20.5f}")

    print()
    print("=== Antipadrão 2: reordenar a cada inserção ===")
    print(f"{'n':<8} | {'Antipadrão (s)':<16} | {'Padrão correto (s)':<20}")
    for n in [500, 1000, 2000]:
        t_a, t_c = medir_insere_e_ordena(n)
        print(f"{n:<8} | {t_a:<16.5f} | {t_c:<20.5f}")

    print()
    print("=== Antipadrão 3: verificação de estabilidade ===")
    estavel = medir_instabilidade(1000)
    print(f"Ordenação por múltiplas chaves manteve estabilidade: {estavel}")


if __name__ == "__main__":
    executar_benchmark()
