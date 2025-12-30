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

    lista_banco = extrair_valores_banco(df_banco, extrado_banco)
    lista_sistema = extrair_valores_sistema(df_sistema, extrado_sistema)

    df_b = pd.DataFrame(lista_banco)
    df_s = pd.DataFrame(lista_sistema)

    df_merged = df_s.merge(df_b, on="indici", how="left")

    inconsistentes = []
    nao_casou = []

    tol = 1e-6
    for _, row in df_merged.iterrows():
        pu_s = row["pu_sistema"]
        pu_b = row["Pu_banco"]

        if pd.isna(pu_b):
            # não encontrou correspondente no banco
            nao_casou.append(
                {
                    "indici": row["indici"],
                    "codigo_investimento": row.get("codigo_investimento"),
                    "PU_Sistema": pu_s,
                    "PU_Banco": None,
                }
            )
        else:
            diff = abs(pu_s - pu_b)
            if diff > tol:
                inconsistentes.append(
                    {
                        "indici": row["indici"],
                        "codigo_investimento": row.get("codigo_investimento"),
                        "PU_Sistema": pu_s,
                        "PU_Banco": pu_b,
                        "Valor_inconsistencias": diff,
                    }
                )

    return inconsistentes, nao_casou


extrato_Banco = "Extrato_Banco.xlsx"
extrato_Sistema = "Extrato_Britech.xlsx"
extrato_Banco_find = buscar_arquivo(extrato_Banco)
extrato_Sistema_find = buscar_arquivo(extrato_Sistema)


if extrato_Banco_find and extrato_Sistema_find:
    extrado_banco = r"./arquivos/Extrato_Banco.xlsx"
    extrado_sistema = r"./arquivos/Extrato_Britech.xlsx"

    resu_inco, resu_nc = analisar_incon(extrado_sistema, extrado_banco)
    print("Valores inconsistentes")
    print(pd.DataFrame(resu_inco))
    print('Valores não correlacionados')
    print(pd.DataFrame(resu_nc))


else:
    print("Ambos os arquivos precisam estar presente")
