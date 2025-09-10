from bcb import sgs
import pandas as pd

def calcular_correcao_ipca(valor_original, data_inicial, data_final):

    try:
        # O código da série do IPCA no SGS é 433
        ipca = sgs.get({'IPCA': 433}, start=data_inicial, end=data_final)

        if ipca.empty:
            print("\nAVISO: Não foram encontrados dados do IPCA para o período selecionado.")
            return None

        fator_acumulado = (1 + ipca['IPCA'] / 100).prod()
        valor_corrigido = valor_original * fator_acumulado

        return valor_corrigido

    except Exception as e:
        print(f"Ocorreu um erro ao buscar os dados ou calcular a correção: {e}")
        return None

def obter_valor():
    #solicita valores
    while True:
            valor_input = input("Valor a ser corrigido: ")
            return float(valor_input)

def obter_data_inicial():
    """Solicita e valida a data inicial do usuário."""
    while True:
        data_input = input("Digite a data INICIAL da cobrança (formato AAAA-MM-DD): ")
        try:
            pd.to_datetime(data_input)
            return data_input
        except ValueError:
            print("Data inválida. Por favor, use o formato AAAA-MM-DD.")

def obter_data_final():
    """Solicita e valida a data final do usuário."""
    while True:
        data_input = input("Digite a data FINAL da cobrança (formato AAAA-MM-DD): ")
        try:
            pd.to_datetime(data_input)
            return data_input
        except ValueError:
            print("Data inválida. Por favor, use o formato AAAA-MM-DD.")


if __name__ == "__main__":
    print("Calculadora de Correção Monetária pelo IPCA")
    print("=" * 40)

    # --- Inserção de dados separada ---
    valor_original = obter_valor()
    data_inicial_input = obter_data_inicial()
    data_final_input = obter_data_final()
    # -----------------------------------

    print("\nCalculando...")
    valor_corrigido = calcular_correcao_ipca(valor_original, data_inicial_input, data_final_input)

    if valor_corrigido is not None:
        print("\n--- Resultado da Correção ---")
        print(f"Valor Original: R$ {valor_original:,.2f}")
        print(f"Período de Correção: de {data_inicial_input} a {data_final_input}")
        print(f"Valor Corrigido pelo IPCA: R$ {valor_corrigido:,.2f}")