import pandas as pd
from pprint import pprint


def pegar_cliente(extrado_banco):
    """
    recebo o caminho da localização do arquivo
    """
    df_sistema = pd.read_excel(extrado_banco, header=None)
    valor = str(df_sistema.iloc[5, 7]).replace(':','').strip()
    cod_cliente = (valor.split('-')[0]).replace('CUST', '').strip()
    linha_carteira = (valor.split('-')[1]).strip()
    return cod_cliente, linha_carteira


def montar_indici_banco(cod_carteira, cod_cliente, sigla, qtd, data_emissao):

    return f"{cod_carteira} | {cod_cliente} | {sigla} | {qtd} | {data_emissao}"


def extrair_valores_banco(df_banco, extrado_banco):
    listao = []
    cliente, linha_carteira = pegar_cliente(extrado_banco)
    for linha in df_banco.index:
        dici = {}
        pu_banco = float(df_banco['PU Atual'][linha])

        
        if pd.isna(pu_banco):
            continue

        qtd = float(df_banco['Qtd.'][linha])
        data_emissao = pd.to_datetime(df_banco['Emissão'][linha], dayfirst=True)
        data_venc = pd.to_datetime(df_banco['Vcto.'][linha], dayfirst=True)

        papel = (df_banco['Papel'][linha]).split('-')[-1].strip()

        dici['indici'] = montar_indici_banco(cliente, linha_carteira, papel, qtd, data_emissao)
        dici['Codigo'] = (df_banco['Código'][linha]).strip()
        dici['Emissao'] = data_emissao
        dici['Venc'] = data_venc
        dici['Qtd'] = qtd
        dici['Pu_banco'] = pu_banco

        listao.append(dici)

    return listao

"""
extrado_banco = r"./arquivos/Extrato_Banco.xlsx"
df_banco = pd.read_excel(extrado_banco, header=22)

pprint(extrair_valores_banco(df_banco, extrado_banco))
"""
