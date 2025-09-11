from bcb import sgs
import pandas as pd
from db import conectar_banco, salvar_calculo, listar_calculos, consultar_calculo


# funcao para calcular a correcao pelo ipca
def calcular_correcao_ipca(valor_original, mes_inicial, ano_inicial, mes_final, ano_final):
    try:
        # monta as datas inicial e final
        data_inicial = pd.to_datetime(f"{ano_inicial}-{mes_inicial:02d}-01")
        data_final = pd.to_datetime(f"{ano_final}-{mes_final:02d}-01") + pd.offsets.MonthEnd(0)

        # busca os dados do ipca no bcb
        ipca = sgs.get({'IPCA': 433}, start=data_inicial, end=data_final)

        # verifica se veio vazio
        if ipca.empty:
            print(f"\nNenhum dado ipca encontrado entre {data_inicial.date()} e {data_final.date()}.")
            return None

        # calcula o fator acumulado e o valor corrigido
        fator_acumulado = (1 + ipca['IPCA'] / 100).prod()
        valor_corrigido = valor_original * fator_acumulado

        return valor_corrigido, fator_acumulado, data_inicial, data_final

    except Exception as e:
        print(f"Erro ao buscar os dados ou calcular a correcao: {e}")
        return None
    

# funcao para pedir mes e ano do usuario
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


# programa principal
if __name__ == "__main__":
    print("Calculadora IPCA (10 calculos obrigatorios)")
    print("=" * 60)

    # conecta ao banco de dados
    con, cur = conectar_banco()

    # faz 10 calculos obrigatorios
    for i in range(1, 11):
        print(f"\n--- Calculo {i} de 10 ---")
        valor_original = float(input("Valor a ser corrigido: ").replace(",", "."))
        mes_inicial, ano_inicial = obter_mes_ano("Digite o mes/ano inicial")
        mes_final, ano_final = obter_mes_ano("Digite o mes/ano final")

        resultado = calcular_correcao_ipca(valor_original, mes_inicial, ano_inicial, mes_final, ano_final)

        if resultado:
            valor_corrigido, fator, di, df = resultado
            # mostra o resultado do calculo
            print("\nResultado:")
            print(f"Valor original: r$ {valor_original:,.2f}")
            print(f"Periodo: {di.strftime('%m/%Y')} a {df.strftime('%m/%Y')}")
            print(f"Fator acumulado: {fator:.8f}")
            print(f"Valor corrigido: r$ {valor_corrigido:,.2f}")
        
            # salva no banco
            salvar_calculo(cur, con, valor_original, mes_inicial, ano_inicial, mes_final, ano_final, fator, valor_corrigido)
            print("[Calculo salvo no banco de dados]")

    # lista os 10 calculos salvos
    print("\n=== Histórico ===")
    historico = listar_calculos(cur)
    for idx, (id_calc, valor) in enumerate(historico, start=1):
        print(f"{idx}. Valor original: R$ {valor:,.2f}")

    # permite consultar um calculo especifico
    while True:
        try:
            escolha = int(input("\nDigite o numero (1-10) do calculo que deseja consultar: "))
            if 1 <= escolha <= 10:
                id_escolhido = historico[escolha-1][0]
                dados = consultar_calculo(cur, id_escolhido) 
                if dados:
                    print("\n--- Consulta detalhada ---")
                    print(f"Id no banco: {dados[0]}")
                    print(f"Valor original: R$ {dados[1]:,.2f}")
                    print(f"Periodo: {dados[2]:02d}/{dados[3]} a {dados[4]:02d}/{dados[5]}")
                    print(f"Fator acumulado: {dados[6]:.8f}")
                    print(f"Valor corrigido: R$ {dados[7]:,.2f}")
                    print(f"Data da consulta: {dados[8]}")
                break
            else:
                print("Escolha invalida, digite de 1 a 10.")
        except ValueError:
            print("Entrada invalida, digite um numero.")
