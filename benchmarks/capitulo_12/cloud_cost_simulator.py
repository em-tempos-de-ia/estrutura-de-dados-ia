"""
Capítulo 12 — O Ciclo de Vida em Produção: Escala, Nuvem e Custo.

Simula o impacto financeiro aproximado da complexidade algorítmica em
faturas de provedores de nuvem serverless, usando a estrutura de
precificação real da AWS Lambda (dois componentes): cobrança por
requisição + cobrança por GB-segundo de duração.

Valores de referência: preços oficiais da AWS Lambda (x86, us-east-1),
consultados em julho de 2026. A AWS pode alterar esses valores; confirme
na página oficial de precificação antes de usar para decisões reais.

Uso:
    python cloud_cost_simulator.py
"""
import math

# Preços oficiais AWS Lambda, x86, us-east-1 (consultado em julho/2026)
PRECO_POR_REQUISICAO = 0.20 / 1_000_000    # $0,20 por 1 milhão de requisições
PRECO_POR_GB_SEGUNDO = 0.0000166667        # $ por GB-segundo (primeiros 6B GB-s/mês)


def calcular_custo_serverless(n_requisicoes, complexidade, memoria_mb=512):
    """
    Simula o custo financeiro aproximado de execução em nuvem, replicando
    a estrutura real de cobrança da AWS Lambda: cobrança por requisição
    MAIS cobrança por GB-segundo de duração.
    """
    if complexidade == "O(1)":
        tempo_ms = 0.5
    elif complexidade == "O(log n)":
        tempo_ms = 0.5 + (math.log2(n_requisicoes) * 0.1)
    elif complexidade == "O(n)":
        tempo_ms = 0.5 + (n_requisicoes * 0.01)
    elif complexidade == "O(n^2)":
        tempo_ms = 0.5 + ((n_requisicoes ** 2) * 0.0001)
    else:
        raise ValueError(f"Complexidade não suportada: {complexidade}")

    tempo_segundos = tempo_ms / 1000.0
    memoria_gb = memoria_mb / 1024.0

    gb_segundos_totais = n_requisicoes * tempo_segundos * memoria_gb
    custo_duracao = gb_segundos_totais * PRECO_POR_GB_SEGUNDO
    custo_requisicoes = n_requisicoes * PRECO_POR_REQUISICAO
    custo_total = custo_duracao + custo_requisicoes

    return tempo_ms, custo_total


if __name__ == "__main__":
    N = 50000
    print("SIMULAÇÃO DE CUSTO EM NUVEM (AWS Lambda, x86, us-east-1)")
    print("Preços consultados em julho de 2026 — confirme na página oficial")
    print(f"Volume de dados (N): {N:,} registros\n")
    print(f"{'Complexidade':<12} | {'Tempo por req (ms)':<19} | {'Custo estimado'}")
    print("-" * 57)
    for c in ["O(1)", "O(log n)", "O(n)", "O(n^2)"]:
        tempo_ms, custo = calcular_custo_serverless(N, c)
        aviso = "  <-- INSUSTENTÁVEL!" if custo > 1000 else ""
        print(f"{c:<12} | {tempo_ms:<19,.2f} | ${custo:,.4f} USD{aviso}")
