"""
Capítulo 11 — Profiling, Testes de Estresse e Auditoria de Código.

Simula um pipeline de dados real, gerado por IA, contendo três
vulnerabilidades assintóticas ocultas (busca O(n) em lista, concatenação de
strings em laço O(k²), inserção no início de lista O(n)), e compara contra
a versão refatorada pelo Programador-Auditor (set + join + deque).

Uso:
    python audit_laboratory.py
"""
import cProfile
import pstats
import random
import statistics
import time
from collections import deque


# --- CÓDIGO DA IA (com vulnerabilidades de performance) -------------------
def processar_pedidos_ia(pedidos, clientes_vip):
    resultados = []
    # ERRO 1: clientes_vip é uma LISTA — 'in' nela dentro do laço é O(n) -> total O(n*m)
    for pedido in pedidos:
        if pedido['cliente_id'] in clientes_vip:
            pedido['desconto'] = 0.15

        # ERRO 2: concatenação de strings em laço cria novos objetos na RAM -> O(k²)
        resumo = ""
        for item in pedido['itens']:
            resumo += item + "; "
        pedido['resumo'] = resumo

        # ERRO 3: inserção no início de uma lista dinâmica -> O(n) a cada passo!
        resultados.insert(0, pedido)

    return resultados


# --- CÓDIGO REFATORADO PELO PROGRAMADOR-AUDITOR ----------------------------
def processar_pedidos_auditor(pedidos, clientes_vip):
    # SOLUÇÃO 1: converte lista de VIPs para set -> busca O(1)
    vips_set = set(clientes_vip)

    # SOLUÇÃO 3: usa deque para inserções O(1) no início
    resultados = deque()

    for pedido in pedidos:
        if pedido['cliente_id'] in vips_set:  # O(1)
            pedido['desconto'] = 0.15

        # SOLUÇÃO 2: usa .join() para construir strings sem realocação -> O(k)
        pedido['resumo'] = "; ".join(pedido['itens']) + "; "

        resultados.appendleft(pedido)  # O(1) no deque

    return list(resultados)


# --- GERADOR DE DADOS DE ESTRESSE ------------------------------------------
def gerar_dados_estresse(n_pedidos, n_vips):
    vips = [f"VIP-{i}" for i in range(n_vips)]
    pedidos = [
        {
            'id': i,
            'cliente_id': f"VIP-{random.randint(0, n_vips * 2)}",
            'itens': [f"Item-{j}" for j in range(10)]
        }
        for i in range(n_pedidos)
    ]
    return pedidos, vips


if __name__ == "__main__":
    pedidos, vips = gerar_dados_estresse(n_pedidos=20000, n_vips=5000)
    pedidos_copia = [dict(p) for p in pedidos]  # cópia para a versão refatorada

    print("Iniciando profiling do código da IA (com vulnerabilidades)...")
    profiler = cProfile.Profile()
    profiler.enable()
    inicio = time.perf_counter()
    processar_pedidos_ia(pedidos, vips)
    tempo_ia = time.perf_counter() - inicio
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats('cumtime')
    print(f"\nTempo total (código da IA): {tempo_ia:.4f} segundos")
    print("\nTop 5 funções mais custosas (cProfile):")
    stats.print_stats(5)

    print("\n" + "=" * 60)
    print("Rodando a versão refatorada pelo Programador-Auditor...")
    inicio = time.perf_counter()
    processar_pedidos_auditor(pedidos_copia, vips)
    tempo_auditor = time.perf_counter() - inicio
    print(f"Tempo total (código refatorado): {tempo_auditor:.4f} segundos")

    print("\n" + "=" * 60)
    print(f"Código não auditado (IA):     ~{tempo_ia:.3f} segundos")
    print(f"Código refatorado (auditor):  ~{tempo_auditor:.3f} segundos")
    print(f"Ganho de desempenho (rodada única): aproximadamente {tempo_ia / tempo_auditor:.1f}x mais rápido")

    # Uma única rodada é sensível a interferência do sistema operacional
    # (outros processos, garbage collection). Pior: a PRIMEIRA rodada de
    # qualquer sessão de medição costuma vir sistematicamente mais lenta
    # (cache frio, alocador de memória "esfriado"), não é ruído aleatório,
    # é viés de aquecimento. Por isso, descartamos uma rodada de aquecimento
    # antes de começar a medir de verdade, e reportamos média e desvio
    # padrão de várias rodadas medidas, não só um único número.
    print("\n" + "=" * 60)
    print("Rodadas de aquecimento (descartadas da medição)...")
    for _ in range(3):
        p_aquec, v_aquec = gerar_dados_estresse(n_pedidos=20000, n_vips=5000)
        p_aquec_copia = [dict(x) for x in p_aquec]
        processar_pedidos_ia(p_aquec, v_aquec)
        processar_pedidos_auditor(p_aquec_copia, v_aquec)

    print("Medindo 10 rodadas independentes após o aquecimento...")
    razoes = []
    for rodada in range(10):
        p, v = gerar_dados_estresse(n_pedidos=20000, n_vips=5000)
        p_copia = [dict(x) for x in p]

        inicio = time.perf_counter()
        processar_pedidos_ia(p, v)
        t_ia = time.perf_counter() - inicio

        inicio = time.perf_counter()
        processar_pedidos_auditor(p_copia, v)
        t_auditor = time.perf_counter() - inicio

        razoes.append(t_ia / t_auditor)

    media = statistics.mean(razoes)
    desvio = statistics.stdev(razoes)
    cv = (desvio / media) * 100
    print(f"Razões observadas: {[f'{r:.1f}x' for r in razoes]}")
    print(f"Média: {media:.1f}x  |  Desvio padrão: {desvio:.1f}x  |  Coeficiente de variação: {cv:.0f}%")
