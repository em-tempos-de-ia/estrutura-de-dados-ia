"""
Capítulo 1 — Big-O na prática: busca ingênua vs. otimizada.

Compara a detecção de músicas duplicadas numa playlist usando:
  - uma solução ingênua O(n²) (laços aninhados + busca linear em lista)
  - uma solução otimizada O(n) (usando set)

Uso:
    python test_stress.py
"""
import time
import random


# Solução sugerida por IA (não auditada)
def encontrar_musicas_duplicadas_ingenua(playlist):
    duplicadas = []
    for i in range(len(playlist)):
        for j in range(i + 1, len(playlist)):
            if playlist[i] == playlist[j]:
                if playlist[i] not in duplicadas:
                    duplicadas.append(playlist[i])
    return duplicadas


# Solução auditada e otimizada
def encontrar_musicas_duplicadas_otimizada(playlist):
    vistas = set()
    duplicadas = set()

    for musica in playlist:
        if musica in vistas:
            duplicadas.add(musica)
        else:
            vistas.add(musica)

    return list(duplicadas)


def executar_benchmark():
    tamanhos = [1000, 5000, 10000, 50000, 100000]

    print(f"{'Tamanho (n)':<12} | {'Ingênuo O(n²) (s)':<20} | {'Otimizado O(n) (s)':<20}")
    print("-" * 58)

    for n in tamanhos:
        # Gera dados simulando nomes de música em uma playlist
        playlist = [f"musica_{random.randint(1, n)}" for _ in range(n)]

        # Medição da solução ingênua
        inicio = time.perf_counter()
        if n <= 10000:  # Limita o O(n²) para evitar travamento do benchmark
            encontrar_musicas_duplicadas_ingenua(playlist)
            tempo_ingenua = f"{time.perf_counter() - inicio:.5f}"
        else:
            tempo_ingenua = "ABORTADO (> 1 min)"

        # Medição da solução otimizada
        inicio = time.perf_counter()
        encontrar_musicas_duplicadas_otimizada(playlist)
        tempo_otimizada = f"{time.perf_counter() - inicio:.5f}"

        print(f"{n:<12} | {tempo_ingenua:<20} | {tempo_otimizada:<20}")


if __name__ == "__main__":
    executar_benchmark()
