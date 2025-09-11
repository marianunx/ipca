import sqlite3

def conectar_banco():
    con = sqlite3.connect("ipca.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS calculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor_original REAL,
        mes_inicial INTEGER,
        ano_inicial INTEGER,
        mes_final INTEGER,
        ano_final INTEGER,
        fator REAL,
        valor_corrigido REAL,
        data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    con.commit()
    return con, cur


def salvar_calculo(cur, con, valor_original, mes_inicial, ano_inicial, mes_final, ano_final, fator, valor_corrigido):
    cur.execute("""
        INSERT INTO calculos (valor_original, mes_inicial, ano_inicial, mes_final, ano_final, fator, valor_corrigido)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (valor_original, mes_inicial, ano_inicial, mes_final, ano_final, fator, valor_corrigido))
    con.commit()


def listar_calculos(cur):
    cur.execute("SELECT id, valor_original FROM calculos ORDER BY id DESC LIMIT 10")
    return cur.fetchall()[::-1]


def consultar_calculo(cur, numero):
    cur.execute("SELECT * FROM calculos WHERE id = ?", (numero,))
    return cur.fetchone()
