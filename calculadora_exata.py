from bcb import sgs
import pandas as pd

def calcular_correcao_ipca(valor_original, mes_inicial, ano_inicial, mes_final, ano_final):
    try:
        # monta as datas no padrão da Calculadora do Cidadão
        data_inicial = pd.to_datetime(f"{ano_inicial}-{mes_inicial:02d}-01")
        data_final = pd.to_datetime(f"{ano_final}-{mes_final:02d}-01") + pd.offsets.MonthEnd(0)

        # busca do IPCA no SGS (código 433)
        ipca = sgs.get({'IPCA': 433}, start=data_inicial, end=data_final)

        if ipca.empty:
            print(f"\nNenhum dado IPCA encontrado entre {data_inicial.date()} e {data_final.date()}.")
            return None

        fator_acumulado = (1 + ipca['IPCA'] / 100).prod()
        valor_corrigido = valor_original * fator_acumulado

        return valor_corrigido, fator_acumulado, data_inicial, data_final

    except Exception as e:
        print(f"Erro ao buscar os dados ou calcular a correção: {e}")
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
                print("Mês inválido. Digite entre 01 e 12.")
        except:
            print("Formato inválido. Use MM/AAAA.")


if __name__ == "__main__":
    print("Calculadora IPCA")
    print("=" * 50)

    valor_original = float(input("Valor a ser corrigido: ").replace(",", "."))

    mes_inicial, ano_inicial = obter_mes_ano("Digite o mês/ano INICIAL")
    mes_final, ano_final = obter_mes_ano("Digite o mês/ano FINAL")

    resultado = calcular_correcao_ipca(valor_original, mes_inicial, ano_inicial, mes_final, ano_final)

    if resultado:
        valor_corrigido, fator, di, df = resultado
        print("\n--- Resultado ---")
        print(f"Valor Original: R$ {valor_original:,.2f}")
        print(f"Período considerado: {di.strftime('%m/%Y')} a {df.strftime('%m/%Y')}")
        print(f"Valor Corrigido pelo IPCA: R$ {valor_corrigido:,.2f}")
        print(f"Valor Corrigido pelo IPCA: R$ {valor_corrigido:,.2f}")
        
        
        
