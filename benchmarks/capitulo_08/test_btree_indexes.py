"""
Capítulo 8 — Conectando Árvores aos Bancos de Dados (B-Tree e B+Tree).

Usa SQLite para criar uma tabela com 1.000.000 de registros sintéticos e
mede a diferença real entre consultas com e sem índice B-Tree.

Uso:
    python test_btree_indexes.py
"""
import sqlite3
import time
import random
import os

DB_PATH = "test_db.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY,
        codigo_transacao TEXT,
        valor REAL,
        status TEXT
    )
""")

print("Gerando 1.000.000 de transações...")
dados = [(f"TRX-{i:07d}", random.uniform(10, 5000), "CONCLUIDO")
         for i in range(1, 1000001)]
cursor.executemany("INSERT INTO transacoes VALUES (NULL, ?, ?, ?)", dados)
conn.commit()

# 1. Consulta SEM índice (Seq Scan — O(n))
alvo = "TRX-0897452"
inicio = time.perf_counter()
cursor.execute("SELECT * FROM transacoes WHERE codigo_transacao = ?", (alvo,))
resultado = cursor.fetchone()
tempo_sem_indice = time.perf_counter() - inicio

# 2. Criando o índice B-Tree
print("Criando índice B-Tree em codigo_transacao...")
inicio_idx = time.perf_counter()
cursor.execute("CREATE INDEX idx_codigo ON transacoes(codigo_transacao)")
tempo_criacao_idx = time.perf_counter() - inicio_idx

# 3. Consulta COM índice B-Tree (Index Scan — O(log n))
inicio = time.perf_counter()
cursor.execute("SELECT * FROM transacoes WHERE codigo_transacao = ?", (alvo,))
resultado_idx = cursor.fetchone()
tempo_com_indice = time.perf_counter() - inicio

print(f"\nConsulta SEM índice (O(n)):     {tempo_sem_indice:.6f} s")
print(f"Tempo para criar B-Tree:        {tempo_criacao_idx:.4f} s")
print(f"Consulta COM B-Tree (O(log n)): {tempo_com_indice:.6f} s")
print(f"Ganho de desempenho: {tempo_sem_indice / tempo_com_indice:.1f}x mais rápido!")

conn.close()
os.remove(DB_PATH)
