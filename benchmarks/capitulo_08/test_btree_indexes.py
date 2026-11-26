import sqlite3
import time
import random
import statistics

random.seed(42)  # semente fixa: mesmos dados e mesmos alvos a cada execução
N = 1_000_000  # número de registros

conn = sqlite3.connect("test_db.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS transacoes")

cursor.execute("""
    CREATE TABLE transacoes (
        id INTEGER PRIMARY KEY,
        codigo_transacao TEXT,
        valor REAL,
        status TEXT
    )
""")

print(f"Gerando {N:,} transações...".replace(",", "."))
dados = [(f"TRX-{i:07d}", random.uniform(10, 5000), "CONCLUIDO")
         for i in range(1, N + 1)]
cursor.executemany("INSERT INTO transacoes VALUES (NULL, ?, ?, ?)", dados)
conn.commit()

alvos = [f"TRX-{random.randint(1, N):07d}" for _ in range(20)]
alvo_exemplo = alvos[0]

plano_antes = cursor.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM transacoes WHERE codigo_transacao = ?",
    (alvo_exemplo,)
).fetchall()
print(f"Plano ANTES do índice: {plano_antes}")

# 1. Consultas SEM índice (Seq Scan — O(n)), repetidas para uma mediana mais estável
tempos_sem_indice = []
for alvo in alvos:
    inicio = time.perf_counter()
    cursor.execute("SELECT * FROM transacoes WHERE codigo_transacao = ?", (alvo,))
    cursor.fetchall()
    tempos_sem_indice.append(time.perf_counter() - inicio)

# 2. Criando o índice B-Tree
print("Criando índice B-Tree em codigo_transacao...")
inicio_idx = time.perf_counter()
cursor.execute("CREATE INDEX idx_codigo ON transacoes(codigo_transacao)")
tempo_criacao_idx = time.perf_counter() - inicio_idx

plano_depois = cursor.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM transacoes WHERE codigo_transacao = ?",
    (alvo_exemplo,)
).fetchall()
print(f"Plano DEPOIS do índice: {plano_depois}")

# 3. Consultas COM índice B-Tree (Index Scan — O(log n)), mesmos alvos
tempos_com_indice = []
for alvo in alvos:
    inicio = time.perf_counter()
    cursor.execute("SELECT * FROM transacoes WHERE codigo_transacao = ?", (alvo,))
    cursor.fetchall()
    tempos_com_indice.append(time.perf_counter() - inicio)

mediana_sem = statistics.median(tempos_sem_indice)
mediana_com = statistics.median(tempos_com_indice)

print(f"\nMediana SEM índice (O(n)):     {mediana_sem:.9f} s")
print(f"Tempo para criar B-Tree:       {tempo_criacao_idx:.4f} s")
print(f"Mediana COM B-Tree (O(log n)): {mediana_com:.9f} s")
print(f"Ganho de desempenho: {mediana_sem / mediana_com:.0f}x mais rápido (mediana de {len(alvos)} consultas)")

conn.close()
