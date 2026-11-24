"""
Capítulo 7 — Árvores e Algoritmos de Busca.

Compara a inserção de 10.000 elementos JÁ ORDENADOS numa BST ingênua (sem
balanceamento) contra uma Árvore AVL autobalanceada, medindo altura final e
tempo de busca.

Convenção de altura (a mesma declarada no capítulo): altura contada em
ARESTAS. Árvore vazia = -1, árvore de um só nó = 0.

Nota: as classes ArvoreAVL e calcular_altura não tinham implementação
completa publicada no corpo do capítulo (só eram citadas na seção "No
Repositório"); a implementação da AVL abaixo é uma AVL padrão (rotações
simples e duplas, Fator de Balanceamento) escrita para este repositório.

Os tempos publicados na Tabela 7.3 do livro foram medidos ANTES de a AVL
receber a política explícita de duplicatas. A correção acrescenta uma
comparação por nó na descida das inserções, o que pode deslocar os tempos de
construção; alturas, contagens de visitas e rotações não mudam, porque as
10.000 chaves do experimento são distintas. Ao republicar os tempos, meça
novamente com esta versão.

Uso:
    python test_trees.py
"""
import platform
import statistics
import subprocess
import sys
import time

sys.setrecursionlimit(100000)

REPETICOES = 3  # a medição é repetida e publica-se a mediana


class No:
    def __init__(self, chave):
        self.chave = chave
        self.esquerdo = None
        self.direito = None


# --- BST ingênua (sem balanceamento) --------------------------------------
# A inserção é a da Listagem 7.1, preservada com seus defeitos para que o
# leitor reproduza a auditoria da seção 7.5 — inclusive a ausência de
# política para chaves duplicadas. A busca usada na medição é a iterativa da
# Listagem 7.2: usar o mesmo algoritmo nas duas estruturas reduz a influência
# de diferenças de implementação e permite destacar o efeito do comprimento
# dos caminhos percorridos. A versão recursiva da Listagem 7.1 está em
# buscar_recursivo, para reproduzir o RecursionError discutido na seção 7.5.
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
        """Busca iterativa, adaptada da Listagem 7.2. Espaço auxiliar O(1)
        na pilha. A Listagem 7.2 devolve o nó encontrado ou None; aqui o
        retorno é booleano, porque o benchmark só precisa saber se a chave
        existe. O caminho percorrido é o mesmo, e é ele que a medição compara.
        """
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return True
            atual = atual.esquerdo if chave < atual.chave else atual.direito
        return False

    def buscar_recursivo(self, no_atual, chave):
        """Busca recursiva (Listagem 7.1). Em árvore degenerada profunda,
        consome um quadro de pilha por nível e estoura o limite de recursão.
        Com o limite padrão do CPython (cerca de 1.000), falha nesta árvore
        de 10.000 nós."""
        if no_atual is None or no_atual.chave == chave:
            return no_atual
        if chave < no_atual.chave:
            return self.buscar_recursivo(no_atual.esquerdo, chave)
        return self.buscar_recursivo(no_atual.direito, chave)


# --- Árvore AVL (autobalanceada) ------------------------------------------
# Altura em arestas, para concordar com a convenção do capítulo: folha = 0,
# subárvore ausente = -1. O Fator de Balanceamento é uma diferença entre
# alturas, portanto a escolha da base não altera a detecção de desequilíbrio.
class NoAVL:
    def __init__(self, chave):
        self.chave = chave
        self.esquerdo = None
        self.direito = None
        self.altura = 0


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def _altura(self, no):
        return no.altura if no else -1

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
        elif chave > no.chave:
            no.direito = self._inserir(no.direito, chave)
        else:
            return no          # política explícita: ignora chaves duplicadas

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
        """Mesma busca iterativa usada na BST, com o mesmo contrato booleano,
        para que a comparação de tempos não misture diferenças de algoritmo."""
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return True
            atual = atual.esquerdo if chave < atual.chave else atual.direito
        return False


def calcular_altura(no):
    """Altura em arestas: árvore vazia = -1, árvore de um só nó = 0."""
    if no is None:
        return -1
    return 1 + max(calcular_altura(no.esquerdo), calcular_altura(no.direito))


def identificar_maquina():
    """Linha de identificação do ambiente, para a medição ser reproduzível."""
    cpu = platform.processor()
    try:
        if sys.platform.startswith("linux"):
            with open("/proc/cpuinfo", encoding="utf-8") as f:
                for linha in f:
                    if "model name" in linha:
                        cpu = linha.split(":", 1)[1].strip()
                        break
        elif sys.platform == "darwin":
            cpu = subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
            ).strip()
    except Exception:
        pass
    return (
        f"Python {platform.python_version()} | "
        f"{platform.system()} {platform.release()} | {platform.machine()}\n"
        f"Processador: {cpu or 'nao identificado'}"
    )


def medir_uma_vez(dados, alvo, n_buscas):
    """Constroi as duas estruturas do zero e mede inserção e busca."""
    bst = ArvoreBinariaIngenua()
    inicio = time.perf_counter()
    for item in dados:
        bst.inserir(item)
    ins_bst = time.perf_counter() - inicio

    avl = ArvoreAVL()
    inicio = time.perf_counter()
    for item in dados:
        avl.inserir(item)
    ins_avl = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for _ in range(n_buscas):
        bst.buscar(alvo)
    busca_bst = (time.perf_counter() - inicio) / n_buscas

    inicio = time.perf_counter()
    for _ in range(n_buscas):
        avl.buscar(alvo)
    busca_avl = (time.perf_counter() - inicio) / n_buscas

    return bst, avl, ins_bst, ins_avl, busca_bst, busca_avl


def executar_benchmark():
    dados_ordenados = list(range(1, 10001))  # 10.000 itens em ordem
    alvo = 10000       # ultima chave inserida: folha mais funda na BST degenerada
    n_buscas = 1000    # a busca e repetida e o tempo dividido pela contagem,
                       # porque uma unica busca nessa escala e rapida demais
                       # para o cronometro medir com precisao confiavel

    print(identificar_maquina())
    print()

    ins_bst, ins_avl, bus_bst, bus_avl = [], [], [], []
    bst = avl = None
    for rep in range(REPETICOES):
        bst, avl, a, b, c, d = medir_uma_vez(dados_ordenados, alvo, n_buscas)
        ins_bst.append(a); ins_avl.append(b)
        bus_bst.append(c); bus_avl.append(d)
        print(f"rodada {rep + 1}/{REPETICOES}: insercao {a:.3f} s / {b:.3f} s | "
              f"busca {c * 1e6:.1f} us / {d * 1e6:.2f} us")
    print()

    med = statistics.median
    alt_bst, alt_avl = calcular_altura(bst.raiz), calcular_altura(avl.raiz)
    razao_ins = med(ins_bst) / med(ins_avl)
    razao_bus = med(bus_bst) / med(bus_avl)

    print(f"Chave buscada: {alvo} (ultima inserida; folha mais funda na BST degenerada)")
    print(f"Medianas de {REPETICOES} execucoes. Alturas em arestas.")
    print()
    print(f"Altura BST ingenua: {alt_bst} (degradada, O(n))")
    print(f"Altura Arvore AVL:  {alt_avl} (balanceada, O(log n))")
    print(f"Insercao das 10.000 chaves  BST: {med(ins_bst):.3f} s | "
          f"AVL: {med(ins_avl):.3f} s ({razao_ins:.0f}x)")
    # tres casas na AVL: com duas, a razao publicada deixa de fechar com os
    # valores da tabela, e um numero que o leitor nao consegue conferir e
    # exatamente o que a secao 7.5 ensina a desconfiar.
    print(f"Busca, media de {n_buscas}      BST: {med(bus_bst) * 1e6:.1f} us | "
          f"AVL: {med(bus_avl) * 1e6:.3f} us ({razao_bus:.0f}x)")


def demonstrar_recursion_error():
    """Mostra o achado da secao 7.5: a busca recursiva da Listagem 7.1
    estoura a pilha numa BST degenerada, com o limite padrao do CPython."""
    bst = ArvoreBinariaIngenua()
    for item in range(1, 10001):
        bst.inserir(item)

    limite_original = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)  # valor tipico de instalacao padrao
    try:
        bst.buscar_recursivo(bst.raiz, 10000)
        print("Busca recursiva concluiu sem erro (limite de recursao alto?)")
    except RecursionError as e:
        print(f"RecursionError, como previsto na secao 7.5: {e}")
    finally:
        sys.setrecursionlimit(limite_original)


if __name__ == "__main__":
    executar_benchmark()
    print()
    print("--- Secao 7.5: busca recursiva em arvore degenerada ---")
    demonstrar_recursion_error()
