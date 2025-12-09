# Analise de Extratos

Este repositório compara dois arquivos Excel: um extrato bancario (`arquivos/Extrato_Banco.xlsx`) e a saida do sistema (`arquivos/Extrato_Britech.xlsx`). O objetivo e listar discrepancias de PU cuja diferenca absoluta seja maior que `1e-6`.

## Como funciona
- `analise.py` carrega os dois Excel (cabecalhos ajustados) e extrai quantidade, datas e PU/valor.
- Os registros sao casados por quantidade e data de vencimento.
- Para cada par, a diferenca `abs(PU_banco - PU_sistema)` e calculada; valores acima da tolerancia (`1e-6`) sao reportados.

## Requisitos
- Python 3
- pandas (`pip install pandas`)

## Execucao
1. Coloque os arquivos em `./arquivos/` com os nomes esperados.
2. Rode:

```bash
python analise.py
```

A saida exibira a lista de inconsistencias encontradas.
