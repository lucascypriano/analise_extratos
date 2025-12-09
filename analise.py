from analisar_banco import extrair_valores_banco
from analisar_sistema import extrair_valores_sistema
from pprint import pprint
import pandas as pd
import os




def buscar_arquivo(nome_arquivo):
    """
    Verifica se o arquivo existe dentro do diretório.
    Retorna True se existir, caso contrário, retorna False.
    """
    diretorio = "./arquivos"
    caminho = os.path.join(diretorio, nome_arquivo)

    if os.path.isfile(caminho):
        return True  # arquivo encontrado
    else:
        return False     # arquivo não existe


def analisar_incon(extrado_sistema, extrado_banco):
    df_sistema = pd.read_excel(extrado_sistema, header=4)
    df_banco = pd.read_excel(extrado_banco, header=22)

    valores_banco = extrair_valores_banco(df_banco, extrado_banco)
    valores_sistema = extrair_valores_sistema(df_sistema, extrado_sistema)
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


extrato_Banco = "Extrato_Banco.xlsx"
extrato_Sistema = "Extrato_Britech.xlsx"
extrato_Banco_find = buscar_arquivo(extrato_Banco)
extrato_Sistema_find = buscar_arquivo(extrato_Sistema)


if extrato_Banco_find and extrato_Sistema_find:
    extrado_banco = r"./arquivos/Extrato_Banco.xlsx"
    extrado_sistema = r"./arquivos/Extrato_Britech.xlsx"

    resu = analisar_incon(extrado_sistema, extrado_banco)
    pprint(resu)

else:
    print("Ambos os arquivos precisam estar presente")
