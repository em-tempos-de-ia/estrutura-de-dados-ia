"""
Suíte de testes unitários automatizados.

Diferente dos scripts em benchmarks/ (que medem VELOCIDADE), esta suíte
verifica CORRETUDE: garante que as estruturas de dados e algoritmos
implementados ao longo do livro se comportam como deveriam, independente
de quão rápido ou devagar isso acontece.

Uso:
    pytest tests/test_exercicios_unitarios.py -v
"""
import sys
import os
import random

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "benchmarks", "capitulo_04"))
sys.path.insert(0, os.path.join(RAIZ, "benchmarks", "capitulo_05"))
sys.path.insert(0, os.path.join(RAIZ, "benchmarks", "capitulo_06"))
sys.path.insert(0, os.path.join(RAIZ, "benchmarks", "capitulo_07"))
sys.path.insert(0, os.path.join(RAIZ, "benchmarks", "capitulo_09"))
sys.path.insert(0, os.path.join(RAIZ, "benchmarks", "capitulo_12"))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))


# ============================================================
# Capítulo 4 — Algoritmos de Ordenação
# ============================================================
class TestCapitulo4Ordenacao:
    def test_merge_sort_ordena_corretamente(self):
        from test_dados_quase_ordenados import merge_sort
        dados = [5, 3, 8, 1, 9, 2, 7, 4, 6, 0]
        assert merge_sort(dados) == sorted(dados)

    def test_merge_sort_lista_vazia(self):
        from test_dados_quase_ordenados import merge_sort
        assert merge_sort([]) == []

    def test_merge_sort_e_estavel(self):
        from test_dados_quase_ordenados import merge_sort
        dados = [(1, "a"), (0, "b"), (1, "c"), (0, "d")]
        resultado = merge_sort(dados)
        # dentro de cada chave igual, a ordem original deve ser preservada
        chave0 = [x[1] for x in resultado if x[0] == 0]
        chave1 = [x[1] for x in resultado if x[0] == 1]
        assert chave0 == ["b", "d"]
        assert chave1 == ["a", "c"]

    def test_quicksort_pivo_ingenuo_ordena_corretamente(self):
        from test_pivo_adversarial import quicksort_pivo_ingenuo
        dados = [5, 3, 8, 1, 9, 2, 7, 4, 6, 0]
        assert quicksort_pivo_ingenuo(dados) == sorted(dados)

    def test_busca_binaria_encontra_elemento_existente(self):
        from test_ordenacao_ingenua import bolha  # garante que o módulo importa
        lista_ordenada = list(range(0, 1000, 2))  # pares de 0 a 998

        def busca_binaria(lista, alvo):
            inicio, fim = 0, len(lista) - 1
            while inicio <= fim:
                meio = (inicio + fim) // 2
                if lista[meio] == alvo:
                    return meio
                elif lista[meio] < alvo:
                    inicio = meio + 1
                else:
                    fim = meio - 1
            return -1

        assert busca_binaria(lista_ordenada, 500) == 250
        assert busca_binaria(lista_ordenada, 501) == -1  # ímpar não existe


# ============================================================
# Capítulo 5 — Pilhas, Filas e Buffers Circulares
# ============================================================
class TestCapitulo5BufferCircular:
    def test_enqueue_dequeue_ordem_fifo(self):
        from test_stacks_queues import BufferCircular
        buf = BufferCircular(capacidade=5)
        for i in range(5):
            buf.enqueue(i)
        for i in range(5):
            assert buf.dequeue() == i

    def test_buffer_cheio_levanta_excecao(self):
        from test_stacks_queues import BufferCircular
        buf = BufferCircular(capacidade=2)
        buf.enqueue(1)
        buf.enqueue(2)
        try:
            buf.enqueue(3)
            assert False, "deveria ter levantado OverflowError"
        except OverflowError:
            pass

    def test_buffer_vazio_retorna_none(self):
        from test_stacks_queues import BufferCircular
        buf = BufferCircular(capacidade=3)
        assert buf.dequeue() is None

    def test_buffer_reaproveita_espaco_apos_dequeue(self):
        from test_stacks_queues import BufferCircular
        buf = BufferCircular(capacidade=2)
        buf.enqueue(1)
        buf.enqueue(2)
        buf.dequeue()
        buf.enqueue(3)  # deve caber, já que um espaço foi liberado
        assert buf.dequeue() == 2
        assert buf.dequeue() == 3


# ============================================================
# Capítulo 6 — Tabelas Hash e Dicionários
# ============================================================
class TestCapitulo6Hash:
    def test_chave_perfeita_encontra_a_si_mesma(self):
        from test_hash_tables import ChavePerfeita
        d = {ChavePerfeita(1): "um", ChavePerfeita(2): "dois"}
        assert d[ChavePerfeita(1)] == "um"

    def test_chave_pessima_ainda_encontra_a_si_mesma(self):
        # apesar do hash degenerado, a busca deve continuar CORRETA,
        # só mais lenta (a corretude não pode ser sacrificada por bug de hash)
        from test_hash_tables import ChavePessima
        d = {ChavePessima(1): "um", ChavePessima(2): "dois"}
        assert d[ChavePessima(1)] == "um"
        assert d[ChavePessima(2)] == "dois"

    def test_chave_pessima_tem_hash_constante(self):
        from test_hash_tables import ChavePessima
        assert hash(ChavePessima(1)) == hash(ChavePessima(2)) == 42


# ============================================================
# Capítulo 7 — Árvores e Algoritmos de Busca
# ============================================================
class TestCapitulo7Arvores:
    def test_bst_insercao_e_busca(self):
        from test_trees import ArvoreBinariaIngenua
        bst = ArvoreBinariaIngenua()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            bst.inserir(v)
        for v in [50, 30, 70, 20, 40, 60, 80]:
            assert bst.buscar(v) is True
        assert bst.buscar(999) is False

    def test_avl_insercao_e_busca(self):
        from test_trees import ArvoreAVL
        avl = ArvoreAVL()
        valores = list(range(1, 101))
        random.Random(7).shuffle(valores)
        for v in valores:
            avl.inserir(v)
        for v in valores:
            assert avl.buscar(v) is True
        assert avl.buscar(-1) is False

    def test_avl_mantem_altura_balanceada(self):
        # a propriedade central da AVL: mesmo inserindo em ordem (o pior
        # caso para uma BST comum), a altura deve ficar próxima de log2(n)
        from test_trees import ArvoreAVL, calcular_altura
        import math
        avl = ArvoreAVL()
        n = 1000
        for v in range(n):
            avl.inserir(v)
        altura = calcular_altura(avl.raiz)
        limite_teorico = 1.44 * math.log2(n + 2)  # cota clássica de altura de AVL
        assert altura <= limite_teorico, (
            f"altura {altura} excede o limite teórico de AVL ({limite_teorico:.1f}) "
            f"para n={n}"
        )


# ============================================================
# Capítulo 9 — Grafos e Redes Complexas
# ============================================================
class TestCapitulo9Grafos:
    def test_matriz_e_lista_representam_as_mesmas_arestas(self):
        from test_graph_representation import criar_grafo_matriz, criar_grafo_lista
        arestas = [(0, 1), (1, 2), (2, 0)]
        matriz = criar_grafo_matriz(3, arestas)
        lista = criar_grafo_lista(3, arestas)

        for a, b in arestas:
            assert matriz[a][b] == 1
            assert matriz[b][a] == 1
            assert b in lista[a]
            assert a in lista[b]

    def test_matriz_simetrica_para_grafo_nao_direcionado(self):
        from test_graph_representation import criar_grafo_matriz
        arestas = [(0, 3), (1, 2)]
        matriz = criar_grafo_matriz(4, arestas)
        for i in range(4):
            for j in range(4):
                assert matriz[i][j] == matriz[j][i]


# ============================================================
# Capítulo 12 — O Ciclo de Vida em Produção
# ============================================================
class TestCapitulo12CustoNuvem:
    def test_o1_e_o_mais_barato(self):
        from cloud_cost_simulator import calcular_custo_serverless
        _, custo_o1 = calcular_custo_serverless(50000, "O(1)")
        _, custo_on2 = calcular_custo_serverless(50000, "O(n^2)")
        assert custo_o1 < custo_on2

    def test_tempo_cresce_com_a_complexidade(self):
        from cloud_cost_simulator import calcular_custo_serverless
        tempos = [
            calcular_custo_serverless(50000, c)[0]
            for c in ["O(1)", "O(log n)", "O(n)", "O(n^2)"]
        ]
        assert tempos == sorted(tempos)  # ordem crescente esperada

    def test_custo_nunca_e_negativo(self):
        from cloud_cost_simulator import calcular_custo_serverless
        for c in ["O(1)", "O(log n)", "O(n)", "O(n^2)"]:
            _, custo = calcular_custo_serverless(1000, c)
            assert custo >= 0


# ============================================================
# Capítulo Bônus — Agentes de IA para Auditoria Automática
# ============================================================
class TestCapituloBonusASTInspector:
    def test_detecta_laco_aninhado(self):
        from ast_inspector import analisar_codigo_fonte
        codigo = """
def funcao_lenta(lista):
    for i in lista:
        for j in lista:
            print(i, j)
"""
        alertas = analisar_codigo_fonte(codigo)
        tipos = [a["tipo"] for a in alertas]
        assert "LACO_ANINHADO" in tipos

    def test_detecta_insert_zero_em_laco(self):
        from ast_inspector import analisar_codigo_fonte
        codigo = """
def funcao_com_bug(dados):
    resultado = []
    for item in dados:
        resultado.insert(0, item)
    return resultado
"""
        alertas = analisar_codigo_fonte(codigo)
        tipos = [a["tipo"] for a in alertas]
        assert "DESLOCAMENTO_MEMORIA_INSERT0" in tipos

    def test_codigo_limpo_nao_gera_alertas(self):
        from ast_inspector import analisar_codigo_fonte
        codigo = """
def funcao_boa(dados):
    return sorted(set(dados))
"""
        alertas = analisar_codigo_fonte(codigo)
        assert alertas == []


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
