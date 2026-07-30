"""
Capítulo 2 — Gerenciamento de Memória e Custo de Execução.

Mede o crescimento de memória de um histórico de reprodução sem limite
(cresce indefinidamente) contra um histórico com buffer limitado (deque
com maxlen), usando tracemalloc da biblioteca padrão.

Uso:
    python test_memoria.py
"""
import tracemalloc
from collections import deque


def sessao_ingenua(n_musicas):
    historico = []
    for i in range(n_musicas):
        historico.append(f"musica_{i}")
    return historico


def sessao_otimizada(n_musicas, tamanho_maximo=50):
    historico = deque(maxlen=tamanho_maximo)
    for i in range(n_musicas):
        historico.append(f"musica_{i}")
    return historico


def medir(func, *args):
    tracemalloc.start()
    func(*args)
    atual, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico / 1024  # KB


if __name__ == "__main__":
    for n in [1000, 10000, 100000]:
        print(f"n={n:<7} ingênua={medir(sessao_ingenua, n):.1f} KB "
              f"otimizada={medir(sessao_otimizada, n):.1f} KB")
