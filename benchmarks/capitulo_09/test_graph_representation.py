import random

SEMENTE = 42  # semente fixa: o mesmo grafo a cada execução

def fmt(n):
    return f"{n:,}".replace(",", ".")

def gerar_arestas(v, p, rng):
    # Cada par de vértices distintos vira aresta com probabilidade p,
    # sem arestas repetidas e sem laços (vértice ligado a si mesmo).
    arestas = []
    for a in range(v):
        for b in range(a + 1, v):
            if rng.random() < p:
                arestas.append((a, b))
    return arestas

def criar_grafo_matriz(v, arestas):
    matriz = [[0] * v for _ in range(v)]
    for a, b in arestas:
        matriz[a][b] = 1
        matriz[b][a] = 1
    return matriz

def criar_grafo_lista(v, arestas):
    lista = [[] for _ in range(v)]
    for a, b in arestas:
        lista[a].append(b)
        lista[b].append(a)"""
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


    return lista

def executar_benchmark():
    v = 2000
    cenarios = [("Esparso", 3 / (v - 1)),  # grau médio esperado: 3
                ("Denso", 0.5)]            # metade dos pares possíveis
    for nome, p in cenarios:
        arestas = gerar_arestas(v, p, random.Random(SEMENTE))
        matriz = criar_grafo_matriz(v, arestas)
        lista = criar_grafo_lista(v, arestas)

        celulas = sum(len(linha) for linha in matriz)  # sempre v * v
        entradas = sum(len(viz) for viz in lista)      # sempre 2 * arestas
        grau_medio = entradas / v

        print(f"Grafo {nome} ({fmt(v)} vértices, {fmt(len(arestas))} arestas):")
        print(f"  Grau médio:          {grau_medio:.2f}".replace(".", ","))
        print(f"  Células na matriz:   {fmt(celulas)}")
        print(f"  Entradas na lista:   {fmt(entradas)}")
        print()

if __name__ == "__main__":
    executar_benchmark()
