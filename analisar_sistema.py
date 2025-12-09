import pandas as pd
from pprint import pprint


def extrair_sigla_britech(descricao: str) -> str:
    """
    Exemplo de DESCRIÇÃO:
    "LFSC - CRA LAFAETE ..."

    Pegamos só "LFSC" (antes do primeiro '-').
    """
    if pd.isna(descricao):
        return ""
    texto = str(descricao).replace('DEBENTURE', '').strip()
    return texto.split()[0].strip()


def montar_indici_britech(extrado_sistema, qtd, data_emissao, desc):
    df_sistema = pd.read_excel(extrado_sistema, header=None)
    cod_carteira = str(df_sistema.iloc[0, 1]).strip()
    linha_carteira = str(df_sistema.iloc[1, 1]).strip()
    sigla = extrair_sigla_britech(desc)
    return f"{cod_carteira} | {linha_carteira} | {sigla} | {qtd} | {data_emissao}"


def extrair_valores_sistema(df_sistema, extrado_sistema):
    listao = []
    for linha in df_sistema.index:
        dici = {}
        qtd = float(df_sistema['QUANTIDADE'][linha])
        data_venc = pd.to_datetime(df_sistema['DATA VENCIMENTO'][linha], dayfirst=True)
        data_emi = pd.to_datetime(df_sistema['DATA EMISSÃO'][linha], dayfirst=True)
        valor_bruto = float(df_sistema['VALOR BRUTO'][linha])
        pu_sistema = float(valor_bruto/qtd)
        mercado = (df_sistema['MERCADO'][linha]).strip()
        desc = str(df_sistema['DESCRIÇÃO'][linha])
        if "TOTAL" == mercado:
            break
        else:
            dici['indici'] = montar_indici_britech(extrado_sistema, qtd, data_emi, desc)
            dici['Venc'] = data_venc
            dici['Valor_bruto'] = valor_bruto
            dici['pu_sistema'] = pu_sistema
            listao.append(dici)

    return listao

"""
extrado_sistema = r"./arquivos/Extrato_Britech.xlsx"
df_sistema = pd.read_excel(extrado_sistema, header=4)


pprint(extrair_valores_sistema(df_sistema, extrado_sistema))
"""
