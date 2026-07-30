# Estruturas de Dados em Tempos de IA — Repositório de Benchmarks

Código de acompanhamento do livro **"Estruturas de Dados em Tempos de IA: De Programador a Auditor"** (Renato Fernando dos Santos).

> **Status deste repositório**: todos os 12 capítulos + Capítulo Bônus têm
> scripts implementados e testados de verdade, e a suíte de testes unitários
> (`tests/test_exercicios_unitarios.py`, 23 testes, todos passando) cobre a
> corretude das principais estruturas implementadas. Ver
> `NOTAS_DE_VALIDACAO.md` para a comparação completa entre os números
> impressos no livro e a execução real — todos os achados foram investigados
> e resolvidos.

## Como executar

```bash
git clone <URL do repositório>
cd estrutura-de-dados-ia
python -m venv venv
source venv/bin/activate    # Linux/macOS
pip install -r requirements.txt

python benchmarks/capitulo_01/test_stress.py
python benchmarks/capitulo_04/test_ordenacao_ingenua.py
python benchmarks/capitulo_04/test_pivo_adversarial.py
python benchmarks/capitulo_04/test_dados_quase_ordenados.py
python benchmarks/capitulo_04/test_padroes_de_erro.py

# Suíte de testes unitários (corretude, não velocidade)
pytest tests/test_exercicios_unitarios.py -v
```

## ⚠️ Antes de rodar: leia isto sobre reprodutibilidade

Os números de tempo de execução impressos no livro são **medidos, não
inventados** — mas medição de tempo de execução é, por natureza, sensível a
fatores que variam de máquina para máquina e de execução para execução. Se
você rodar um script uma única vez e o número não bater com o do livro,
**isso é esperado, não é sinal de dado fabricado**. O que deve se manter
estável é a *ordem de grandeza* (dezenas, centenas, milhares de vezes),
não a segunda casa decimal.

**Achado específico que vale saber antes de rodar `benchmarks/capitulo_11/audit_laboratory.py`**:
investigamos por que esse benchmark em particular variava demais entre
execuções (de 5x a mais de 100x de "ganho") e descobrimos que **a primeira
vez que uma função roda dentro de um processo Python é sistematicamente
mais lenta** do que as chamadas seguintes — provavelmente o alocador de
memória do Python reservando blocos novos na primeira vez, e reaproveitando
nas seguintes. Testamos até com 25 segundos de intervalo entre execuções
isoladas, e o efeito não desaparece: não é o computador "esfriando", é o
processo Python "esquentando" e ficando assim enquanto estiver de pé.

Por isso, `audit_laboratory.py` descarta 3 rodadas de aquecimento antes de
medir de verdade, e reporta média ± desvio padrão de 10 rodadas, não um
único número de uma única execução. **Se você for adaptar algum script
deste repositório, ou escrever o seu próprio benchmark, aplique a mesma
prática**: descarte as primeiras execuções, meça várias vezes, e reporte
média com desvio padrão (ou pelo menos faixa mínimo-máximo) em vez de um
número isolado. Detalhes completos de cada achado de reprodutibilidade
estão em `NOTAS_DE_VALIDACAO.md`.

## Licença

Código licenciado sob a Licença MIT — ver Ficha Técnica e Créditos do livro.
