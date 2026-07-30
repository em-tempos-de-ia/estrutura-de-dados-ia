"""
Capítulo 7 — Árvores e Algoritmos de Busca.

Compara a inserção de 10.000 elementos JÁ ORDENADOS numa BST ingênua (sem
balanceamento) contra uma Árvore AVL auto-balanceada, medindo altura final
e tempo de busca.

Nota: as classes ArvoreAVL e calcular_altura não tinham implementação
completa publicada no corpo do capítulo (só eram citadas na seção "No
Repositório"); a implementação da AVL abaixo é uma AVL padrão (rotações
simples e duplas, Fator de Balanceamento) escrita para este repositório.

Uso:
    python test_trees.py
"""
import time
import sys

sys.setrecursionlimit(100000)


class No:
    def __init__(self, chave):
        self.chave = chave
        self.esquerdo = None
        self.direito = None


# --- BST ingênua (sem balanceamento), como mostrada no corpo do capítulo --
class ArvoreBinariaIngenua:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave):
        if self.raiz is None:
            self.raiz = No(chave)
        else:
            self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave):
        if chave < no_atual.chave:
            if no_atual.esquerdo is None:
                no_atual.esquerdo = No(chave)
            else:
                self._inserir_recursivo(no_atual.esquerdo, chave)
        else:
            if no_atual.direito is None:
                no_atual.direito = No(chave)
            else:
                self._inserir_recursivo(no_atual.direito, chave)

    def buscar(self, chave):
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return True
            atual = atual.esquerdo if chave < atual.chave else atual.direito
        return False


# --- Árvore AVL (auto-balanceada) -----------------------------------------
class NoAVL:
    def __init__(self, chave):
        self.chave = chave
        self.esquerdo = None
        self.direito = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def _altura(self, no):
        return no.altura if no else 0

    def _fator_balanceamento(self, no):
        return self._altura(no.esquerdo) - self._altura(no.direito) if no else 0

    def _atualizar_altura(self, no):
        no.altura = 1 + max(self._altura(no.esquerdo), self._altura(no.direito))

    def _rotacao_direita(self, y):
        x = y.esquerdo
        t2 = x.direito
        x.direito = y
        y.esquerdo = t2
        self._atualizar_altura(y)
        self._atualizar_altura(x)
        return x

    def _rotacao_esquerda(self, x):
        y = x.direito
        t2 = y.esquerdo
        y.esquerdo = x
        x.direito = t2
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        return y

    def inserir(self, chave):
        self.raiz = self._inserir(self.raiz, chave)

    def _inserir(self, no, chave):
        if no is None:
            return NoAVL(chave)
        if chave < no.chave:
            no.esquerdo = self._inserir(no.esquerdo, chave)
        else:
            no.direito = self._inserir(no.direito, chave)

        self._atualizar_altura(no)
        fb = self._fator_balanceamento(no)

        # Caso Esquerda-Esquerda
        if fb > 1 and chave < no.esquerdo.chave:
            return self._rotacao_direita(no)
        # Caso Direita-Direita
        if fb < -1 and chave >= no.direito.chave:
            return self._rotacao_esquerda(no)
        # Caso Esquerda-Direita
        if fb > 1 and chave >= no.esquerdo.chave:
            no.esquerdo = self._rotacao_esquerda(no.esquerdo)
            return self._rotacao_direita(no)
        # Caso Direita-Esquerda
        if fb < -1 and chave < no.direito.chave:
            no.direito = self._rotacao_direita(no.direito)
            return self._rotacao_esquerda(no)

        return no

    def buscar(self, chave):
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return True
            atual = atual.esquerdo if chave < atual.chave else atual.direito
        return False


def calcular_altura(no):
    if no is None:
        return 0
    return 1 + max(calcular_altura(no.esquerdo), calcular_altura(no.direito))


def executar_benchmark():
    dados_ordenados = list(range(1, 10001))  # 10.000 itens em ordem

    # Teste 1: BST ingênua
    bst = ArvoreBinariaIngenua()
    inicio = time.perf_counter()
    for item in dados_ordenados:
        bst.inserir(item)
    tempo_insercao_bst = time.perf_counter() - inicio

    # Teste 2: Árvore AVL (balanceada)
    avl = ArvoreAVL()
    inicio = time.perf_counter()
    for item in dados_ordenados:
        avl.inserir(item)
    tempo_insercao_avl = time.perf_counter() - inicio

    print(f"Altura BST ingênua: {calcular_altura(bst.raiz)} (degradada, O(n))")
    print(f"Altura Árvore AVL:  {calcular_altura(avl.raiz)}    (balanceada, O(log n))")
    print(f"Tempo de inserção BST: {tempo_insercao_bst:.5f}s")
    print(f"Tempo de inserção AVL: {tempo_insercao_avl:.5f}s")
    print()

    alvo = 10000  # pior caso para a BST degradada: o último elemento inserido (folha mais funda)
    n_buscas = 1000  # média de várias buscas: uma única busca nessa escala é rápida
                      # demais para o cronômetro medir com precisão confiável

    inicio = time.perf_counter()
    for _ in range(n_buscas):
        bst.buscar(alvo)
    tempo_busca_bst = (time.perf_counter() - inicio) / n_buscas

    inicio = time.perf_counter()
    for _ in range(n_buscas):
        avl.buscar(alvo)
    tempo_busca_avl = (time.perf_counter() - inicio) / n_buscas

    razao = tempo_busca_bst / tempo_busca_avl if tempo_busca_avl > 0 else float("inf")
    print(f"Tempo médio de busca na BST ({n_buscas} buscas): {tempo_busca_bst:.8f} segundos")
    print(f"Tempo médio de busca na AVL ({n_buscas} buscas): {tempo_busca_avl:.8f} segundos ({razao:.0f}x mais rápida)")


if __name__ == "__main__":
    executar_benchmark()
