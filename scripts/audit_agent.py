"""
Capítulo Bônus — Agentes de IA para Auditoria Automática.

Une a análise estática (AST) ao disparo do modelo de linguagem, produzindo
um relatório de auditoria em JSON.
"""
import json
from ast_inspector import analisar_codigo_fonte
from agent_prompts import PROMPT_SISTEMA_AUDITOR


# ATENÇÃO: esta função é um MOCK (simulação) para fins didáticos.
# Ela NÃO chama nenhum provedor de IA de verdade — apenas devolve uma
# resposta fixa, para que você possa testar o fluxo completo do agente
# sem precisar de credenciais de API. Em produção, substitua o corpo
# desta função pela chamada ao SDK do provedor de LLM de sua escolha,
# mantendo a mesma assinatura (mesma entrada, mesmo formato de saída).
def chamar_llm_auditora(codigo: str, alertas_ast: list) -> dict:
    prompt_usuario = f"""
    CÓDIGO PARA AUDITORIA:
    ```python
    {codigo}
    ```

    ALERTAS DETECTADOS VIA AST:
    {json.dumps(alertas_ast, indent=2)}
    """

    print("[Agente Auditor] Processando análise semântica e estrutural...")

    # Resposta simulada (mock) — troque por uma chamada real de API aqui
    resposta_mock = {
        "aprovado": len(alertas_ast) == 0,
        "complexidade_original": "O(n²)" if alertas_ast else "O(n)",
        "complexidade_refatorada": "O(n)",
        "diagnostico": "Identificado laço aninhado e busca linear sobre coleção mutável.",
        "codigo_refatorado": "# Solução auditada e otimizada\n..."
    }
    return resposta_mock


def auditar_arquivo(caminho_arquivo: str):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    print(f"=== AUDITANDO: {caminho_arquivo} ===")

    # 1. Análise estática
    alertas = analisar_codigo_fonte(codigo)
    print(f"Alertas AST encontrados: {len(alertas)}")
    for a in alertas:
        print(f"  - Linha {a['linha']} [{a['tipo']}]: {a['mensagem']}")

    # 2. Análise semântica (mock, ver aviso acima)
    resultado = chamar_llm_auditora(codigo, alertas)
    return resultado


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        resultado = auditar_arquivo(sys.argv[1])
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        print("Uso: python audit_agent.py <arquivo.py>")
