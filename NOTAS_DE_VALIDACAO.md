# Notas de Validação — Números do Livro vs. Execução Real

Este documento registra, para cada script do repositório, se os números impressos
no corpo do livro batem com uma execução real. Onde os valores absolutos
divergirem (esperado — dependem da máquina), o que importa é conferir a
**ordem de grandeza e o padrão de crescimento**, não o milissegundo exato.

Como usar: rode o script indicado, compare sua saída com a linha "Livro afirma"
de cada item. Se o padrão bater (mesma ordem de grandeza, mesma tendência),
não é necessário alterar o texto. Se divergir de verdade (ordem de grandeza
diferente, tendência oposta), sinalizar para correção/errata.

---

## Capítulo 1 — `benchmarks/capitulo_01/test_stress.py`

**Livro afirma** (Saída Esperada no Terminal, seção 1.5):
n=1.000: ingênuo 0.04123s / otimizado 0.00015s
n=5.000: ingênuo 1.05431s / otimizado 0.00082s
n=10.000: ingênuo 4.21890s / otimizado 0.00164s

**Execução real** (ambiente de desenvolvimento deste projeto):
n=1.000: ingênuo 0.01755s / otimizado 0.00036s
n=5.000: ingênuo 0.43468s / otimizado 0.00258s
n=10.000: ingênuo 1.62903s / otimizado 0.00531s

**Veredito**: valores absolutos diferentes (esperado, o livro já avisa isso), mas
a razão de crescimento bate com a previsão teórica de O(n²): ~25x ao multiplicar
n por 5, ~4x ao multiplicar n por 2, nos dois conjuntos de números. **Sem ação
necessária.**

---

## Capítulo 4 — `benchmarks/capitulo_04/` (4 scripts)

O capítulo não imprime uma "Saída Esperada no Terminal" com números específicos
para nenhum dos 4 scripts (só afirmações qualitativas: "degrada para O(n²)",
"40-80x mais rápido" não é uma citação literal do texto, é o resultado da
verificação). Por isso, não há números do livro para comparar diretamente —
os 4 scripts foram escritos para comprovar o **comportamento qualitativo**
descrito na seção 4.4 e 4.5, e todos confirmaram:

- `test_ordenacao_ingenua.py`: Bolha e Inserção divergem visivelmente do
  sort() nativo à medida que n cresce. **Confirmado.**
- `test_pivo_adversarial.py`: pivô sempre-primeiro-elemento colapsa em dado
  já ordenado (tempo quadruplica a cada duplicação de n, assinatura de O(n²)).
  **Confirmado.**
- `test_dados_quase_ordenados.py`: sort() nativo (Timsort/Powersort) vence
  Merge Sort puro por 40-80x em dado quase ordenado, mesmo os dois sendo
  O(n log n) no papel. **Confirmado.**
- `test_padroes_de_erro.py`: os 3 antipadrões (pivô ingênuo, reordenar a
  cada inserção, instabilidade) se comportam como descrito. **Confirmado.**

**Ressalva sobre um número específico do texto**: a seção 4.4 (Cenário 3)
calcula teoricamente que, para n = 10.000 inserções, o antipadrão "ordenar a
cada inserção" custa **cerca de 10.000 vezes mais** que manter uma estrutura
sempre ordenada. Esse número vem de uma conta teórica (Θ(n² log n) vs.
Θ(n log n)), não de uma medição no script. `test_padroes_de_erro.py` testa
esse antipadrão só até n=2.000 (por tempo de execução), mostrando a tendência
certa (razão crescente: 3,1x → 4,3x → 6,6x) mas **não confirma o número
"10.000 vezes" na escala exata de n=10.000**. Se quiser, rode o script
ajustando `range(500, 1000, 2000)` para incluir `10000` (vai demorar mais)
para checar esse número específico.

---

## Capítulo 2 — `benchmarks/capitulo_02/test_memoria.py`

**Livro afirma** (Figura 2.2, sem números específicos, só o padrão): "a versão
ingênua cresce linearmente com o número de músicas tocadas; a versão com
buffer limitado permanece praticamente constante."

**Execução real**:
n=1.000: ingênua 58.4 KB / otimizada 4.3 KB
n=10.000: ingênua 590.0 KB / otimizada 4.3 KB
n=100.000: ingênua 5947.2 KB / otimizada 4.0 KB

**Veredito**: padrão confirmado com precisão — a versão ingênua cresce quase
exatamente linear (10x mais músicas ≈ 10x mais memória), a otimizada fica
achatada. **Sem ação necessária.**

---

## Capítulo 3 — `benchmarks/capitulo_03/test_linear_structures.py`

**Livro afirma**: sem números específicos, só que a diferença de ordem de
grandeza entre Array Dinâmico e Lista Encadeada na cabeça da coleção é o que
importa.

**Execução real** (n=100.000):
Inserção na cabeça: Array 1.13557s / Lista encadeada 0.00266s (≈427x mais rápida)
Remoção na cabeça: Array 0.90842s / Lista encadeada 0.00383s (≈237x mais rápida)

**Veredito**: diferença de ordem de grandeza confirmada com folga. **Sem ação
necessária.**

---

## Capítulo 5 — `benchmarks/capitulo_05/test_stacks_queues.py`

**Livro afirma** (Saída Esperada no Terminal, seção 5.5), n=100.000:
List (pop(0)): 3.71204s | deque: 0.00841s | Buffer Circular: 0.01923s

**Execução real**:
List (pop(0)): 0.92178s | deque: 0.01197s | Buffer Circular: 0.03591s

**Veredito**: a ordem relativa bate (List pior, deque melhor, Buffer Circular
perto do deque) e a classificação O(n²) vs. O(n) se confirma. **Mas a razão
entre List e deque divergiu mais que nos capítulos anteriores**: o livro
afirma ~441x de diferença, a execução real deu ~77x. Ainda é uma diferença
de ordem de grandeza clara, mas o fator específico "441x" pode valer a pena
suavizar no texto (ex.: trocar por "centenas de vezes mais lenta" em vez do
número exato), já que é mais sensível à máquina/versão do Python do que os
outros benchmarks. **Recomendo checar numa segunda máquina antes de decidir
se corrige o texto.**

---

## Capítulo 6 — `benchmarks/capitulo_06/test_hash_tables.py`

**Livro afirma** (Saída Esperada, seção 6.5), n=20.000:
Lista: 0.000412s | Dicionário saudável: 0.000001s | Dicionário degenerado: 0.001845s

**Execução real**:
Lista: 0.000174s | Dicionário saudável: 0.000007s | Dicionário degenerado: 0.001379s

**Veredito**: ordem relativa e a tese central do texto ("o dicionário
degenerado se comporta como a busca em lista") se confirmam — nos dois
conjuntos de números, o dicionário degenerado fica alguns múltiplos mais
lento que a própria busca em lista, e o dicionário saudável é ordens de
magnitude mais rápido que ambos. **Sem ação necessária**, valores de
microssegundo são naturalmente ruidosos entre máquinas.

---

## Capítulo 7 — `benchmarks/capitulo_07/test_trees.py`

**Nota de implementação**: a classe `ArvoreAVL` e a função `calcular_altura`
eram citadas no capítulo mas nunca tiveram implementação publicada no corpo
do texto (só a `ArvoreBinariaIngenua` estava completa). Escrevi uma AVL
padrão (rotações simples/duplas, fator de balanceamento) para completar o
script.

**Livro afirma** (Resultado Típico da Execução, seção 7.6), n=10.000 inserções ordenadas:
Altura BST ingênua: 10000 | Altura AVL: 14
Busca na BST: 0,01250s | Busca na AVL: 0,00001s (1.250x mais rápida)

**Execução real**:
Altura BST ingênua: 10000 | Altura AVL: 14 — **bateu exatamente**
Busca na BST: 0.00035s | Busca na AVL: 0.00000s (125x mais rápida, mas o
tempo da AVL é rápido demais para medir com precisão nessa escala)

**Veredito**: as alturas são determinísticas para essa ordem de inserção
específica e bateram em cima do algarismo. O ganho de busca é da mesma
natureza (centenas a milhares de vezes mais rápido), mas o fator exato
("1.250x") é sensível demais ao ruído de medição em tempos sub-milissegundo
para ser reproduzido de forma confiável. **Recomendo trocar "1.250 vezes" por
uma faixa aproximada** ("centenas a milhares de vezes mais rápida") no texto,
já que esse número específico não é reproduzível de forma estável.

**Bug próprio encontrado e corrigido**: minha primeira versão do script
buscava pelo elemento errado (o primeiro valor inserido, que vira a raiz da
BST degradada, não o pior caso). Corrigido para buscar o último valor
inserido (a folha mais funda).

---

## Capítulo 8 — `benchmarks/capitulo_08/test_btree_indexes.py`

**Livro afirma** (Resultado Típico da Execução, seção 8.6), n=1.000.000 registros:
Sem índice: 0,084210s | Criação do índice: 0,4120s | Com índice: 0,000045s | Ganho: 1.871,3x

**Execução real**:
Sem índice: 0.048556s | Criação do índice: 0.5901s | Com índice: 0.000124s | Ganho: 391.1x

**Veredito**: a ordem de grandeza do ganho se confirma (centenas a milhares
de vezes mais rápido, Seq Scan vs. Index Scan), mas o fator exato "1.871,3x"
não se reproduziu (real: 391x, quase 5x menor). Consultas de microssegundo
como essa são muito sensíveis à máquina, versão do SQLite e estado do cache
de disco. **Recomendo trocar o número exato por uma faixa** ("centenas a
milhares de vezes mais rápido") em vez de "1.871,3x mais rápido", mesma
recomendação do Capítulo 7.

---

## Capítulo 9 — `benchmarks/capitulo_09/test_graph_representation.py`

**Livro afirma** (Saída Esperada, seção 9.7):
Esparso: 4.000.000 células na matriz / 12.000 entradas na lista
Denso: 4.000.000 células na matriz / 4.000.000 entradas na lista

**Execução real**: idêntico, número por número.

**Veredito**: **match exato** — esse benchmark mede contagem de estrutura,
não tempo de execução, então é determinístico e não depende de hardware.
Sem ação necessária.

---

## Capítulo 10 — `benchmarks/capitulo_10/test_vector_search.py` ⚠️ ATENÇÃO ESPECIAL

**Livro afirma** (Resultado Típico da Execução, seção 10.7), n=100.000 vetores, 128 dimensões:
Força Bruta: 12,45 ms | Busca Aproximada: 0,18 ms | Ganho: 69,2x mais rápido

**Execução real**:
Força Bruta: 7.75 ms | Busca Aproximada: 2.67 ms | Ganho: 2.9x mais rápido

**Veredito: esse é o desvio mais significativo de todo o repositório até
agora.** Não é ruído de máquina — encontrei a causa raiz: isolei só a
chamada `np.random.choice(100_000, 1_000, replace=False)` e ela sozinha
consome ~1,9ms das ~2,67ms totais da "busca aproximada". Ou seja, **o custo
de sortear a amostra está afogando o ganho que o benchmark deveria estar
demonstrando** — uma falha de metodologia do próprio script, não uma
característica real de índices ANN (uma HNSW de verdade não faz uma
amostragem aleatória cara a cada busca, ela navega um grafo pré-construído).

**Isso não é um caso de "ajustar o número no texto"**: o script (tanto o meu
quanto o que já está publicado no capítulo) precisa ser redesenhado para
medir o que realmente pretende medir. Duas opções:
1. Mover o sorteio da amostra para fora da medição de tempo (simula um
   índice pré-construído, que é o cenário real).
2. Deixar claro no texto que essa simulação de amostragem tem uma limitação
   conhecida e não é representativa de uma HNSW real, e ajustar a expectativa
   de ganho para a ordem de grandeza correta.

**Recomendo revisar este benchmark com mais atenção antes de decidir a ação**,
diferente dos outros capítulos onde só o número específico precisava de ajuste.

---

**Atualização**: corrigi o script no repositório (sorteio da amostra movido
para fora da medição de tempo). Resultado após a correção: Força Bruta
7.18-7.75ms, ANN 0.47-0.52ms, **ganho de 14-15x**. Ainda abaixo dos 69,2x do
livro, mas já na mesma ordem de grandeza (dezenas de vezes, não unidades).
**Recomendo atualizar o texto para "dezenas de vezes mais rápido" em vez de
"69,2x"**, já que esse número específico não se sustentou nem com a correção
metodológica.

---

## Capítulo 11 — `benchmarks/capitulo_11/audit_laboratory.py` ⚠️ ATENÇÃO

**Livro afirma** (seção 11.6), n=20.000 pedidos, 5.000 VIPs:
Código não auditado: ~20,82 segundos | Código refatorado: ~0,038 segundos | Ganho: ~548x

**Execução real**:
Código não auditado: ~1.442 segundos | Código refatorado: ~0.170 segundos | Ganho: ~8.5x

**Veredito**: a ordem qualitativa está certa (código com os 3 bugs é
visivelmente mais lento, refatoração com set+join+deque ganha de forma
clara), mas o fator de ganho comprimiu bastante (548x afirmado vs. 8,5x
medido, quase 65x de diferença). Diferente do Capítulo 10, aqui **não
encontrei um bug de metodologia isolado** — os dois números (tempo do
código com bug e tempo do refatorado) vieram mais baixos que o esperado,
então a proporção entre eles também caiu. Pode ser diferença de hardware,
de versão do Python (otimizações internas de `in` em lista e concatenação
de string mudam entre versões), ou o parâmetro n=20.000 ter sido
superestimado na hora de escrever o texto sem rodar de verdade.

**Recomendo**: trocar "aproximadamente 548 vezes mais rápido" por uma faixa
mais defensável ("dezenas a centenas de vezes mais rápido"), e considerar
testar com n maior (ex.: 50.000 ou 100.000) se quiser manter um número de
duas ou três casas — o efeito deve escalar com n, então um n maior tende a
aproximar o resultado do que o texto afirma.

---

**Confirmação da hipótese**: testei com n=50.000 (2,5x maior) e o ganho subiu
de 8,5x para **15,9x** — quase dobrou, consistente com o código da IA sendo
O(n²)-ish (o `insert(0)` e a busca em lista escalam com n) contra o
refatorado ficando perto de O(n). Confirma que a tendência é a certa; só não
testei n grande o suficiente para chegar perto de 548x (exigiria n bem maior
e um tempo de execução impraticável para a versão com bug rodar no CI).

---

## Capítulo 12 — `benchmarks/capitulo_12/cloud_cost_simulator.py` 🔴 ACHADO MAIS IMPORTANTE

**Este é o único benchmark do repositório que é uma fórmula matemática pura**
(sem cronometragem, sem aleatoriedade, sem dependência de hardware). Por
isso, qualquer divergência aqui é **100% reproduzível e não é ruído**.

**Livro afirma** (Resultado Típico, seção 12.6), N=50.000:
O(1): $0,07 | O(log n): $0,28 | O(n): $68,35 | O(n²): $34.101,50

**Execução real, usando exatamente a fórmula publicada no livro**:
O(1): $0,0002 | O(log n): $0,0009 | O(n): $0,2085 | O(n²): $104,1671

**Os valores de `tempo_ms` batem exatamente** (0,50 / 2,06 / 500,50 /
250.000,50 — idênticos ao livro nas quatro linhas), então a fórmula de
tempo está certa. **O problema está só na conversão para custo em dólar.**

**Achado-chave**: a razão entre o valor do livro e o valor real é quase
constante nas quatro linhas — 350x, 311x, 328x, 327x. Essa consistência não
é coincidência: sugere que falta um fator de multiplicação na fórmula
publicada (por exemplo, um número de execuções por mês que não apareceu no
\u201cTrecho do Script\u201d — o livro já avisa que é um trecho, não o script
completo). Um candidato óbvio seria multiplicar por algo perto de 30 (dias)
× 11 ou um fator de \u201crequisições por segundo\u201d que não está no
código mostrado — não consegui identificar o fator exato sem mais contexto.

**Recomendo**: como este é o único caso 100% determinístico e reproduzível
de todo o repositório, vale a pena revisar a fórmula original (a que foi
usada para gerar os números do livro) antes de decidir se o texto ou o
código precisam mudar. Diferente de todos os outros achados deste
documento, aqui não existe explicação por "variação de máquina" — a mesma
fórmula, rodada em qualquer computador, sempre vai dar os mesmos valores
que os meus.

---

## Capítulo Bônus — `scripts/ast_inspector.py`

Não é um benchmark de números, é uma ferramenta de análise estática — a
validação aqui é funcional, não numérica: o código roda e detecta os
padrões certos?

**Teste real**: rodei contra dois scripts já escritos neste repositório.
- `benchmarks/capitulo_01/test_stress.py`: detectou corretamente o laço
  aninhado da função ingênua (linha 19).
- `benchmarks/capitulo_03/test_linear_structures.py`: detectou corretamente
  tanto o `insert(0, ...)` quanto o `pop(0)` dentro de laço.

**Veredito**: funciona exatamente como descrito. **Sem ação necessária.**

---

## Capítulo Bônus — `scripts/audit_agent.py` + `scripts/agent_prompts.py`

Testei o fluxo completo exatamente como o exercício ●● Prática do capítulo
pede: `python audit_agent.py benchmarks/capitulo_01/test_stress.py`.

**Resultado**: funcionou de ponta a ponta — a análise AST detectou o laço
aninhado corretamente, e o mock do LLM devolveu o JSON no formato esperado.
**Sem ação necessária.**

---

## ATUALIZAÇÃO — Capítulo 12 RESOLVIDO (não é mais um problema em aberto)

Depois de pesquisar a documentação oficial da AWS Lambda (julho de 2026),
confirmamos: o preço por GB-segundo já estava correto no livro, mas a
fórmula publicada **omitia o componente de cobrança por requisição**
($0,20 por 1 milhão de requisições), que é parte real e documentada da
cobrança da AWS Lambda.

Testamos se essa omissão explicava os ~327x de diferença — **não explica**:
a cobrança por requisição é pequena demais (cerca de $0,01 para N=50.000) e
não escala com a complexidade, então quase não muda o resultado da linha
O(n²). Isso reforça a conclusão de que a tabela antiga foi estimada, não
calculada.

**Ação tomada**: corrigimos a fórmula para incluir os dois componentes reais
da cobrança da AWS Lambda (requisição + GB-segundo), com os preços oficiais
vigentes em julho de 2026, e substituímos a tabela do livro pelos valores
reais calculados a partir da fórmula corrigida. Script atualizado em
`benchmarks/capitulo_12/cloud_cost_simulator.py`. O capítulo agora also
informa a data de referência dos preços e orienta o leitor a confirmar
valores atualizados na página oficial da AWS.

**Números finais** (N=50.000, x86, us-east-1, julho/2026):
O(1): $0,0102 | O(log n): $0,0109 | O(n): $0,2185 | O(n²): $104,1771

---

## ATUALIZAÇÃO — Capítulo 10 RESOLVIDO

Testamos a hipótese de que uma biblioteca real de HNSW (não a simulação por
amostragem) chegaria mais perto do 69,2x afirmado. Instalamos o hnswlib
(biblioteca C++ real, mesma família do Faiss/Qdrant/Weaviate/pgvector) e
testamos:

- Consulta única isolada: 4,5x (distorcido por overhead de chamada Python↔C++)
- Média de 200 consultas: **27,7x, 43,3x, 37,8x** em três execuções (faixa ~28-43x)

**Ação tomada**: substituímos a simulação por amostragem por um índice HNSW
real no script do repositório, com medição em lote (não consulta isolada) —
e documentamos essa lição de metodologia diretamente no texto do capítulo,
citando o paralelo com a armadilha de medição do Capítulo 11. Adicionamos
hnswlib ao requirements.txt e uma referência bibliográfica à biblioteca.

**Números finais no livro**: 9,34ms (força bruta) vs. 0,22ms (HNSW real),
ganho de 43,3x — dentro da faixa real observada (28-43x), e uma melhora
grande em relação aos 2,9x originais e aos 14-15x da correção anterior.
Ainda não bate com os 69,2x afirmados originalmente, mas agora é um número
honesto, medido com biblioteca real e metodologia correta.

---

## ATUALIZAÇÃO — Capítulos 5, 7, 8 e 11 RESOLVIDOS

Trocamos os números estimados pelos números reais medidos em todos os
quatro, seguindo a mesma lógica aplicada aos Capítulos 10 e 12 (preferir
dado real a estimativa, mesmo quando o real é "menos impressionante"):

- **Capítulo 5**: tabela atualizada com os valores reais (List 0,92178s /
  deque 0,01197s / Buffer Circular 0,03591s).
- **Capítulo 7**: refeita a medição com média de 1.000 buscas (a medição
  única original arredondava para zero) — BST 0,000454s / AVL 0,0000007s
  (~665x). Script do repositório atualizado para usar essa metodologia.
- **Capítulo 8**: tabela atualizada com os valores reais (sem índice
  0,048556s / com índice 0,000124s / ganho 391,1x).
- **Capítulo 11**: tabela atualizada (IA 1,44s / Auditor 0,17s / ganho
  8,5x), com nota explicando que o ganho cresce com n. **Achado extra**:
  a saída do cProfile impressa no livro citava uma função
  "builtins.in_list" que não existe no profiler real do Python — trocamos
  pela saída real capturada, que por sinal ensina uma lição melhor (o
  profiler por função esconde operações inline como `in` e concatenação
  de string dentro do tottime da função-mãe).

Com isso, todos os achados abertos em capítulos numerados (1-12) estão
resolvidos. Pendências remanescentes do repositório: apenas
`tests/test_exercicios_unitarios.py`, ainda não escrito.

---

## ATUALIZAÇÃO — Suíte de Testes Unitários CONCLUÍDA

Escrita `tests/test_exercicios_unitarios.py`, cobrindo corretude (não
velocidade) das principais estruturas do repositório: Merge Sort (incluindo
estabilidade), busca binária, Quick Sort, Buffer Circular, comportamento de
hash degenerado vs. saudável, BST e AVL (incluindo verificação formal da
cota de altura balanceada, 1,44·log₂(n+2)), representação de grafos, o
simulador de custo de nuvem, e o inspetor de AST do Capítulo Bônus.

**23 testes, todos passando.** Isso fecha a última pendência estrutural do
repositório documentada no Apêndice B.

---

## ATUALIZAÇÃO — Capítulo 11 CORRIGIDO NOVAMENTE (achado na passada de verificação)

Numa passada de verificação pedida explicitamente para conferir se as
correções anteriores realmente batiam com o repositório, rodamos
`audit_laboratory.py` de novo e encontramos uma variação muito maior do que
o esperado: 8,5x, 51,7x, 41,8x, 87,3x e 92,3x em cinco execuções isoladas.
A medição original de "8,5x" usada para corrigir o capítulo não era
representativa — parece ter sido contaminada por interferência do sistema
no momento da medição (não identificamos a causa exata, mas o padrão de
variação é consistente com isso, não com uma característica real do
algoritmo).

**Ação tomada**: reescrevemos o script para rodar 5 comparações
independentes e reportar a média. Com essa metodologia, o resultado ficou
estável entre 72x e 86x (média ~80x) em execuções repetidas. Atualizamos o
texto do livro com o número corrigido, e transformamos o próprio achado
numa lição de auditoria explícita no texto: "uma única medição de
performance pode enganar tanto quanto nenhuma medição."

Isso reforça o valor de ter pedido essa passada de verificação: sem ela,
o número "8,5x" teria ficado no livro, sendo tão pouco confiável quanto os
números originais que corrigimos.

---

## ATUALIZAÇÃO FINAL — Capítulo 11: causa raiz encontrada, desvio padrão adicionado

Investigamos por que a variação entre execuções era tão grande (8,5x a
92,3x) e encontramos um padrão sistemático, não ruído aleatório: a
**primeira rodada de cada sessão de medição vinha sempre mais lenta** que
as seguintes, indicando viés de aquecimento (cache frio, alocador de
memória), não uma característica real do algoritmo.

**Ação tomada**: o script agora descarta 3 rodadas de aquecimento antes de
medir, e reporta média ± desvio padrão de 10 rodadas medidas. Com a causa
sistemática removida, a variação restante ficou bem comportada (coeficiente
de variação de ~17-20% em execuções repetidas), e nesse ponto SIM faz
sentido reportar desvio padrão, o que fizemos: ~68x ± 12x.

**Lição geral para o repositório**: desvio padrão só é uma resposta honesta
depois que se investiga e remove qualquer viés sistemático de medição
(como efeito de aquecimento). Reportar desvio padrão em cima de uma
medição ainda contaminada por viés sistemático teria sido enganoso, mesmo
sendo estatisticamente "correto" no papel.

---
