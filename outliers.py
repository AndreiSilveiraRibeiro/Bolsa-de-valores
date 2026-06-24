import pandas as pd
import numpy as np
from scipy import stats

tabela_final = pd.read_csv("tbl_final_limpo.csv")
tabela_indicadores = pd.read_csv("tbl_indicadores_limpo.csv")

print(tabela_final.describe())
print(tabela_final)

tabela_final['z-score'] = stats.zscore(tabela_final['patrimonio_inicial'])

z_score = tabela_final

Q1 = tabela_final['cotacao'].quantile(0.25)
Q3 = tabela_final['cotacao'].quantile(0.75)
IQR = Q3 - Q1

limite_alto = Q3 + (1.5 * IQR)
limite_baixo = Q1 - (1.5 * IQR)

media = tabela_final['cotacao'].mean()
tabela_final['cotacao'] = np.where(tabela_final['cotacao'] > limite_alto, media, tabela_final['cotacao'])

outliers = z_score[z_score['z-score'] > 1].copy()
ranking_outliers = outliers.sort_values(by='z-score', ascending=False)
ranking_outliers['posicao_ranking'] = range(1, len(ranking_outliers) + 1)

correlacao = tabela_final['rentabilidade_dia'].corr(tabela_final['cotacao'], method='spearman')

print(f"\nCorrelação entre rentabilidade por dia e cotação: {correlacao}")

# ===== Visualizando o Top 10 Maiores Outliers da Base =====

print("\n===== TOP 10 MAIORES OUTLIERS DETECTADOS =====")
colunas_exibicao = ['posicao_ranking', 'nome_fundo', 'categoria', 'data_cota', 'cotacao', 'z-score']
print(ranking_outliers[colunas_exibicao].head(10).to_string(index=False))

# Exportar a tabela limpa para o Power BI
tabela_final.to_csv("tbl_final_processada.csv", index=False)
# Exportar o ranking de outliers para a aba de Auditoria do seu Dashboard
ranking_outliers[colunas_exibicao].to_csv("ranking_outliers_auditoria.csv", index=False)

print("\nProcessamento concluído. Arquivos 'tbl_final_processada.csv' e 'ranking_outliers_auditoria.csv' gerados.")