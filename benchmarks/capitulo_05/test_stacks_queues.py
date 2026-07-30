"""
Capítulo 5 — Pilhas, Filas e Buffers Circulares.

Simula o envio e processamento de 100.000 mensagens comparando três
abordagens: fila por lista padrão, fila por deque, e fila por buffer
circular com array fixo.

Uso:
    python test_stacks_queues.py
"""
import time
from collections import deque


class BufferCircular:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.buffer = [None] * capacidade
        self.head = 0
        self.tail = 0
        self.tamanho = 0

    def enqueue(self, item):
        if self.tamanho == self.capacidade:
            raise OverflowError("Buffer cheio")
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.capacidade
        self.tamanho += 1

    def dequeue(self):
        if self.tamanho == 0:
            return None
        item = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.capacidade
        self.tamanho -= 1
        return item


def executar_benchmark():
    n = 100000
    print(f"Executando estresse com {n:,} operações de enqueue + dequeue...\n")

    # 1. Lista padrão (ingênua)
    inicio = time.perf_counter()
    fila_lista = []
    for i in range(n):
        fila_lista.append(i)
    while len(fila_lista) > 0:
        fila_lista.pop(0)
    tempo_lista = time.perf_counter() - inicio

    # 2. Deque (otimizado)
    inicio = time.perf_counter()
    fila_deque = deque()
    for i in range(n):
        fila_deque.append(i)
    while len(fila_deque) > 0:
        fila_deque.popleft()
    tempo_deque = time.perf_counter() - inicio

    # 3. Buffer circular fixo
    inicio = time.perf_counter()
    buffer_circular = BufferCircular(n)
    for i in range(n):
        buffer_circular.enqueue(i)
    while buffer_circular.tamanho > 0:
        buffer_circular.dequeue()
    tempo_circular = time.perf_counter() - inicio

    print(f"{'Implementação':<25} | {'Tempo (s)':<14} | {'Complexidade'}")
    print("-" * 56)
    print(f"{'List (pop(0))':<25} | {tempo_lista:<14.5f} | O(n²)")
    print(f"{'collections.deque':<25} | {tempo_deque:<14.5f} | O(n)")
    print(f"{'Buffer Circular':<25} | {tempo_circular:<14.5f} | O(n)")


if __name__ == "__main__":
    executar_benchmark()
