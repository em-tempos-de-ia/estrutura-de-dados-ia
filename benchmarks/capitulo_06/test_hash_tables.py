"""
Capítulo 6 — Tabelas Hash e Dicionários.

Compara busca sequencial em lista O(n), busca em dicionário com hash
saudável O(1), e busca em dicionário com função hash degenerada (forçando
colisão total, O(n) mesmo sendo um dicionário).

Uso:
    python test_hash_tables.py
"""
import time


class ChavePessima:
    """Simula um objeto com função hash degenerada (sempre colide)."""
    def __init__(self, valor):
        self.valor = valor

    def __hash__(self):
        return 42  # força TODOS os objetos a caírem no mesmo bucket!

    def __eq__(self, outro):
        return isinstance(outro, ChavePessima) and self.valor == outro.valor


class ChavePerfeita:
    """Simula um objeto com bom espalhamento de hash."""
    def __init__(self, valor):
        self.valor = valor

    def __hash__(self):
        return hash(self.valor)

    def __eq__(self, outro):
        return isinstance(outro, ChavePerfeita) and self.valor == outro.valor


def executar_benchmark():
    n = 20000
    print(f"Iniciando teste com {n:,} registros...\n")

    lista_dados = list(range(n))
    dict_perfeito = {ChavePerfeita(i): True for i in range(n)}
    dict_pessimo = {ChavePessima(i): True for i in range(n)}

    alvo = n - 1  # pior caso de busca (último elemento)

    # 1. Busca sequencial em lista — O(n)
    inicio = time.perf_counter()
    encontrado = alvo in lista_dados
    tempo_lista = time.perf_counter() - inicio

    # 2. Busca em dicionário saudável — O(1)
    chave_busca_boa = ChavePerfeita(alvo)
    inicio = time.perf_counter()
    encontrado = chave_busca_boa in dict_perfeito
    tempo_dict_bom = time.perf_counter() - inicio

    # 3. Busca em dicionário colidido — O(n)
    chave_busca_ruim = ChavePessima(alvo)
    inicio = time.perf_counter()
    encontrado = chave_busca_ruim in dict_pessimo
    tempo_dict_ruim = time.perf_counter() - inicio

    print(f"{'Estrutura':<32} | {'Tempo (s)':<14} | {'Complexidade'}")
    print("-" * 62)
    print(f"{'Busca em lista':<32} | {tempo_lista:<14.6f} | O(n)")
    print(f"{'Dicionário saudável':<32} | {tempo_dict_bom:<14.6f} | O(1) médio")
    print(f"{'Dicionário degenerado':<32} | {tempo_dict_ruim:<14.6f} | O(n) pior caso")


if __name__ == "__main__":
    executar_benchmark()
