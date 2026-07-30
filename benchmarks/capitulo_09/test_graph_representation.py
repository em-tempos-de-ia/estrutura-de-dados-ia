"""
Capítulo 9 — Grafos e Redes Complexas.

Compara o uso de memória (em células/entradas ocupadas) entre Matriz e
Lista de Adjacência, em um grafo esparso e um grafo denso.

Uso:
    python test_graph_representation.py
"""
import random


def criar_grafo_matriz(v, arestas):
    matriz = [[0] * v for _ in range(v)]
    for a, b in arestas:
        matriz[a][b] = 1
        matriz[b][a] = 1
    return matriz


def criar_grafo_lista(v, arestas):
    lista = {i: [] for i in range(v)}
    for a, b in arestas:
        lista[a].append(b)
        lista[b].append(a)
    return lista


def gerar_arestas_esparsas(v, grau_medio=3):
    return [(random.randrange(v), random.randrange(v)) for _ in range(v * grau_medio)]


def gerar_arestas_densas(v, proporcao=0.5):
    total = int(v * v * proporcao)
    return [(random.randrange(v), random.randrange(v)) for _ in range(total)]


def executar_benchmark():
    v = 2000
    esparsas = gerar_arestas_esparsas(v)
    densas = gerar_arestas_densas(v)

    for nome, arestas in [("Esparso", esparsas), ("Denso", densas)]:
        matriz = criar_grafo_matriz(v, arestas)
        lista = criar_grafo_lista(v, arestas)

        tam_matriz = v * v  # células ocupadas, independente do nº de arestas
        tam_lista = sum(len(viz) for viz in lista.values())

        print(f"Grafo {nome} ({v} vértices, {len(arestas)} arestas):")
        print(f"  Células na matriz:     {tam_matriz:,}")
        print(f"  Entradas na lista:     {tam_lista:,}")
        print()


if __name__ == "__main__":
    executar_benchmark()
