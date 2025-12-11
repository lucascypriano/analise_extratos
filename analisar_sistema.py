import pandas as pd
import re
from pprint import pprint


def extrair_sigla_britech(descricao: str) -> str:
    """
    Exemplo de DESCRIÇÃO:
      "DEBENTURE ITSA24 -  Vcto: 15-07-2025 -> ..."

    Queremos extrair "ITSA" (sem o 24).
    Também funciona para:
      - "DEBENTURE RDORB9 ..." -> "RDORB"
      - "DEBENTURE KLBNA2 ..." -> "KLBNA"
      - "LFSC Bradesco ..."    -> "LFSC"
      - "NTN-B - Vcto ..."     -> "NTN-B"
    """
    if pd.isna(descricao):
        return ""

    # remove a palavra DEBENTURE (maiúscula/minúscula)
    texto = str(descricao).replace('DEBENTURE', '').replace('Debenture', '').strip()

    # pega o primeiro "token" (antes do espaço)
    primeiro = texto.split()[0].strip()  # ex: ITSA24, RDORB9, NTN-B

    # remove somente dígitos do final, mantendo letras e hífen
    # ITSA24  -> ITSA
    # RDORB9 -> RDORB
    # KLBNA2 -> KLBNA
    # NTN-B  -> NTN-B (não tem dígito no fim)
    m = re.match(r'([A-Za-z\-]+)', primeiro)
    if m:
        return m.group(1)

    return primeiro


def montar_indici_britech(extrado_sistema, qtd, data_venc, desc):
    df_sistema = pd.read_excel(extrado_sistema, header=None)
    cod_carteira = str(df_sistema.iloc[0, 1]).strip()
    linha_carteira = str(df_sistema.iloc[1, 1]).strip()
    sigla = extrair_sigla_britech(desc)
    return f"{cod_carteira} | {linha_carteira} | {sigla} | {qtd} | {data_venc}"


def extrair_valores_sistema(df_sistema, extrado_sistema):
    listao = []
    for linha in df_sistema.index:
        dici = {}
        qtd = float(df_sistema['QUANTIDADE'][linha])
        valor_bruto = float(df_sistema['VALOR BRUTO'][linha])
        pu_sistema = float(valor_bruto/qtd)
        mercado = (df_sistema['MERCADO'][linha]).strip()
        desc = str(df_sistema['DESCRIÇÃO'][linha])
        data_emi = pd.to_datetime(
            df_sistema.loc[linha, "DATA EMISSÃO"], dayfirst=True, errors="coerce"
        )
        data_venc = pd.to_datetime(
            df_sistema.loc[linha, "DATA VENCIMENTO"], dayfirst=True, errors="coerce"
        )
        data_venc_chave = data_venc.date()

        if "TOTAL" == mercado:
            break
        else:
            dici['indici'] = montar_indici_britech(extrado_sistema, qtd, data_venc_chave, desc)
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
