"""
Capítulo Bônus — Agentes de IA para Auditoria Automática.

Navega pela árvore sintática (AST) de um código Python e detecta dois
padrões anti-performance clássicos: laços aninhados (O(n²) ou pior) e uso
de pop(0)/insert(0, x) em listas dentro de laços (O(n) por iteração).
"""
import ast


class AnalisadorAST(ast.NodeVisitor):
    def __init__(self):
        self.alertas = []
        self.profundidade_loop_atual = 0

    def visit_For(self, node):
        self.profundidade_loop_atual += 1
        if self.profundidade_loop_atual > 1:
            self.alertas.append({
                "tipo": "LACO_ANINHADO",
                "linha": node.lineno,
                "mensagem": f"Laço 'for' aninhado (profundidade {self.profundidade_loop_atual}). "
                             f"Risco de complexidade O(n²)."
            })
        self.generic_visit(node)
        self.profundidade_loop_atual -= 1

    def visit_While(self, node):
        self.profundidade_loop_atual += 1
        if self.profundidade_loop_atual > 1:
            self.alertas.append({
                "tipo": "LACO_ANINHADO",
                "linha": node.lineno,
                "mensagem": "Laço 'while' aninhado. Risco de complexidade O(n²)."
            })
        self.generic_visit(node)
        self.profundidade_loop_atual -= 1

    def visit_Call(self, node):
        # Detecta lista.pop(0) ou lista.insert(0, v) dentro de laços
        if isinstance(node.func, ast.Attribute):
            nome_metodo = node.func.attr
            if nome_metodo == "pop" and self.profundidade_loop_atual > 0:
                if node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == 0:
                    self.alertas.append({
                        "tipo": "DESLOCAMENTO_MEMORIA_POP0",
                        "linha": node.lineno,
                        "mensagem": "pop(0) dentro de laço: custo O(n) por iteração. "
                                     "Use collections.deque."
                    })
            elif nome_metodo == "insert" and self.profundidade_loop_atual > 0:
                if node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == 0:
                    self.alertas.append({
                        "tipo": "DESLOCAMENTO_MEMORIA_INSERT0",
                        "linha": node.lineno,
                        "mensagem": "insert(0, ...) dentro de laço: custo O(n) por iteração. "
                                     "Use collections.deque."
                    })
        self.generic_visit(node)


def analisar_codigo_fonte(codigo: str):
    tree = ast.parse(codigo)
    analisador = AnalisadorAST()
    analisador.visit(tree)
    return analisador.alertas


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            codigo = f.read()
        alertas = analisar_codigo_fonte(codigo)
        if not alertas:
            print(f"Nenhum padrão anti-performance encontrado em {sys.argv[1]}.")
        for a in alertas:
            print(f"[{a['tipo']}] linha {a['linha']}: {a['mensagem']}")
    else:
        print("Uso: python ast_inspector.py <arquivo.py>")
