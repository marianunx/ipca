from bcb import sgs
import pandas as pd

def calcular_correcao_ipca(valor_original, data_inicial, data_final):
    try:
        # Consulta do IPCA (433)
        ipca = sgs.get({'IPCA': 433}, start=data_inicial, end=data_final)

        if ipca.empty:
            print(f"\nNenhum dado IPCA encontrado entre {data_inicial.date()} e {data_final.date()}.")
            return None

        fator_acumulado = (1 + ipca['IPCA'] / 100).prod()
        valor_corrigido = valor_original * fator_acumulado

        return valor_corrigido, fator_acumulado

    except Exception as e:
        print(f"Erro ao buscar os dados ou calcular a correção: {e}")
        return None, None


def obter_valor():
    while True:
        valor_input = input("Valor a ser corrigido: ")
        try:
            return float(valor_input.replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número válido.")


def obter_data(mensagem):
    while True:
        data_input = input(mensagem)
        try:
            return pd.to_datetime(data_input)
        except ValueError:
            print("Data inválida. Use o formato AAAA-MM-DD.")


if __name__ == "__main__":
    print("Calculadora de Correção Monetária pelo IPCA")
    print("=" * 40)

    valor_original = obter_valor()
    data_inicial = obter_data("Digite a data INICIAL da cobrança (AAAA-MM-DD): ")
    data_final = obter_data("Digite a data FINAL da cobrança (AAAA-MM-DD): ")

    if data_inicial > data_final:
        print("Erro: a data inicial não pode ser posterior à data final.")
        exit(1)

    print("\nCalculando...")
    valor_corrigido, fator = calcular_correcao_ipca(valor_original, data_inicial, data_final)

    if valor_corrigido is not None:
        print("\n--- Resultado ---")
        print(f"Valor Original: R$ {valor_original:,.2f}")
        print(f"Período: de {data_inicial.date()} a {data_final.date()}")
        print(f"Fator acumulado: {fator:.6f}")
        print(f"Valor Corrigido pelo IPCA: R$ {valor_corrigido:,.2f}")
