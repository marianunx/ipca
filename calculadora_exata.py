from bcb import sgs
import pandas as pd
from db import conectar_banco, salvar_calculo, listar_calculos, consultar_calculo
import tkinter as tk
from tkinter import simpledialog, messagebox

# funcao para calcular a correcao pelo ipca
def calcular_correcao_ipca(valor_original, mes_inicial, ano_inicial, mes_final, ano_final):
    try:
        data_inicial = pd.to_datetime(f"{ano_inicial}-{mes_inicial:02d}-01")
        data_final = pd.to_datetime(f"{ano_final}-{mes_final:02d}-01") + pd.offsets.MonthEnd(0)

        ipca = sgs.get({'IPCA': 433}, start=data_inicial, end=data_final)

        if ipca.empty:
            print(f"\nNenhum dado ipca encontrado entre {data_inicial.date()} e {data_final.date()}.")
            return None

        fator_acumulado = (1 + ipca['IPCA'] / 100).prod()
        valor_corrigido = valor_original * fator_acumulado

        return valor_corrigido, fator_acumulado, data_inicial, data_final

    except Exception as e:
        print(f"Erro ao buscar os dados ou calcular a correcao: {e}")
        return None
    
def obter_mes_ano(mensagem):
    while True:
        entrada = input(mensagem + " (MM/AAAA): ")
        try:
            mes, ano = entrada.split("/")
            mes, ano = int(mes), int(ano)
            if 1 <= mes <= 12:
                return mes, ano
            else:
                print("Mês invalido. digite entre 01 e 12.")
        except:
            print("Formato invalido. use mm/aaaa.")

# função popup para consultar cálculo

def popup_consulta(historico, cur):
    root = tk.Tk()
    root.withdraw()  # esconde a janela principal

    # monta o texto dos valores
    texto_valores = "\n".join([f"{idx+1}. R$ {valor:,.2f}" for idx, (id_calc, valor) in enumerate(historico)])

    escolha = simpledialog.askinteger(
        "Consulta de cálculo",
        f"Histórico de cálculos:\n{texto_valores}\n\nDigite o número do cálculo que deseja consultar:"
    )

    if escolha and 1 <= escolha <= len(historico):
        id_escolhido = historico[escolha-1][0]
        dados = consultar_calculo(cur, id_escolhido)
        if dados:
            _, valor_original, mi, ai, mf, af, fator, valor_corrigido, data_consulta = dados
            mensagem = (
                f"Valor original: R$ {valor_original:,.2f}\n"
                f"Período: {mi:02d}/{ai} a {mf:02d}/{af}\n"
                f"Fator acumulado: {fator:.8f}\n"
                f"Valor corrigido: R$ {valor_corrigido:,.2f}\n"
                f"Data da consulta: {data_consulta}"
            )
            messagebox.showinfo("Detalhes do cálculo", mensagem)
    root.destroy()

# programa principal

if __name__ == "__main__":
    print("Calculadora IPCA (10 calculos obrigatorios)")
    print("=" * 60)

    con, cur = conectar_banco()

    for i in range(1, 11):
        print(f"\n--- Cálculo {i} de 10 ---")
        valor_original = float(input("Valor a ser corrigido: ").replace(",", "."))
        mes_inicial, ano_inicial = obter_mes_ano("Digite o mes/ano inicial")
        mes_final, ano_final = obter_mes_ano("Digite o mes/ano final")

        resultado = calcular_correcao_ipca(valor_original, mes_inicial, ano_inicial, mes_final, ano_final)

        if resultado:
            valor_corrigido, fator, di, df = resultado
            print("\nResultado:")
            print(f"Valor original: r$ {valor_original:,.2f}")
            print(f"Período: {di.strftime('%m/%Y')} a {df.strftime('%m/%Y')}")
            print(f"Fator acumulado: {fator:.8f}")
            print(f"Valor corrigido: r$ {valor_corrigido:,.2f}")

            salvar_calculo(cur, con, valor_original, mes_inicial, ano_inicial, mes_final, ano_final, fator, valor_corrigido)
            print("[Cálculo salvo no banco de dados]")

    # lista os 10 cálculos
    historico = listar_calculos(cur)

    # abre popup para consultar
    popup_consulta(historico, cur)
