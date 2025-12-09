import pandas as pd
from pprint import pprint

extrado_banco = r"./arquivos/Extrato_Banco.xlsx"
extrado_sistema = r"./arquivos/Extrato_Britech.xlsx"

df_sistema = pd.read_excel(extrado_sistema, header=4)
df_banco = pd.read_excel(extrado_banco, header=22)

def extrair_valores_banco():
    listao = []
    for linha in df_banco.index:
        dici = {}
        pu_banco = float(df_banco['PU Atual'][linha])
        qtd = float(df_banco['Qtd.'][linha])

        data_emissao = pd.to_datetime(df_banco['Emissão'][linha], dayfirst=True)
        data_venc = pd.to_datetime(df_banco['Vcto.'][linha], dayfirst=True)

        dici['indici'] = f"{qtd} | {data_venc}"
        dici['Codigo'] = (df_banco['Código'][linha]).strip()
        dici['Emissao'] = data_emissao
        dici['Venc'] = data_venc
        dici['Qtd'] = qtd
        dici['Pu_banco'] = pu_banco

        if pd.isna(pu_banco):
            continue
        else:
            listao.append(dici)

    return listao


def extrair_valores_sistema():
    listao = []
    for linha in df_sistema.index:
        dici = {}
        qtd = float(df_sistema['QUANTIDADE'][linha])
        data_venc = pd.to_datetime(df_sistema['DATA VENCIMENTO'][linha], dayfirst=True)
        valor_bruto = float(df_sistema['VALOR BRUTO'][linha])
        pu_sistema = float(valor_bruto/qtd)
        mercado = (df_sistema['MERCADO'][linha]).strip()
        if "TOTAL" == mercado:
            break
        else:
            dici['indici'] = f"{qtd} | {data_venc}"
            dici['Venc'] = data_venc
            dici['Valor_bruto'] = valor_bruto
            dici['pu_sistema'] = pu_sistema
            listao.append(dici)

    return listao


def analisar_incon():
    valores_banco = extrair_valores_banco()
    valores_sistema = extrair_valores_sistema()
    lista_inconsistencia = []

    TOL = 1e-6  # tolerância
    for vbi in valores_banco:
        indici_banco = vbi['indici']

        for vsi in valores_sistema:
            indici_sistema = vsi['indici']
            if indici_banco == indici_sistema:
                pu_sistema = vsi['pu_sistema']
                break

        dif = abs(vbi['Pu_banco'] - pu_sistema)

        if dif > TOL:
            lista_inconsistencia.append(
                {
                    'codigo_investimento': vbi['Codigo'],
                    'PU_Sistema': pu_sistema,
                    'PU_Banco': vbi['Pu_banco'],
                    'Valor_inconsistencias': dif,
                }
            )

    return lista_inconsistencia


pprint(analisar_incon())
