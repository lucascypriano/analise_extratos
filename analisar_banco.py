import pandas as pd
import re
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


def montar_indici_banco(cod_carteira, cod_cliente, sigla, qtd, data_venc):
    return f"{cod_carteira} | {cod_cliente} | {sigla} | {qtd} | {data_venc}"


def extrair_valores_banco(df_banco, extrado_banco):
    listao = []
    cliente, linha_carteira = pegar_cliente(extrado_banco)

    papel_atual = None  # guarda o "CRA", "DBNCI", "DEBNC" etc do bloco atual

    for linha in df_banco.index:
        dici = {}

        # ==== 1) Atualiza o papel_atual com base na coluna "Código" ====
        codigo = str(df_banco['Código'][linha]).strip()

        # quando encontrar "Negociação", o papel do bloco é o Código da linha seguinte
        if codigo == "Negociação":
            proxima_linha = linha + 1
            if proxima_linha in df_banco.index:
                papel_atual = str(df_banco['Código'][proxima_linha]).strip()

        # ==== 2) Pega PU; se for NaN, nem monta registro ====
        pu_banco = df_banco['PU Atual'][linha]
        if pd.isna(pu_banco):
            continue
        pu_banco = float(pu_banco)

        qtd = float(df_banco['Qtd.'][linha])

        data_emissao = pd.to_datetime(df_banco['Emissão'][linha], dayfirst=True)
        data_venc = pd.to_datetime(df_banco['Vcto.'][linha], dayfirst=True)

        # só a parte da data para a chave:
        data_venc_chave = data_venc.date()

        # ==== 3) Definir o "papel" dessa linha ====
        # emitente pode ser útil na exceção DEBNC
        emitente = df_banco['Emitente'][linha]
        if pd.isna(emitente):
            emitente = ""
        else:
            emitente = str(emitente).strip()

        papel = papel_atual  # padrão: usa o papel do bloco

        # Se o código for Bxxxxx / BXxxxxx, aplicamos as regras:
        # (B426064, B730378, BX12345, etc.)
        if codigo.startswith('B'):
            if papel_atual == "DEBNC" and emitente:
                # exceção: bloco DEBNC usa o Emitente (ITSA, KLBN, etc.)
                papel = emitente
            else:
                papel = papel_atual

        # Se por algum motivo ainda não tiver papel, pula
        if not papel:
            continue

        # Se tiver hífen no texto do papel, pega a parte depois do hífen
        # (caso você ainda queira manter esse comportamento)
        if '-' in papel:
            papel_final = papel.split('-')[-1].strip()
        else:
            papel_final = papel.strip()

        # ==== 4) Monta o índice e o dicionário final ====
        dici['indici'] = montar_indici_banco(
            cliente,
            linha_carteira,
            papel_final,
            qtd,
            data_venc_chave
        )

        dici['Codigo'] = codigo
        dici['Emissao'] = data_emissao
        dici['Venc'] = data_venc_chave
        dici['Qtd'] = qtd
        dici['Pu_banco'] = pu_banco

        listao.append(dici)

    return listao

"""
extrado_banco = r"./arquivos/Extrato_Banco.xlsx"
df_banco = pd.read_excel(extrado_banco, header=22)

pprint(extrair_valores_banco(df_banco, extrado_banco))
"""
