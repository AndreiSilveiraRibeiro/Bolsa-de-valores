import pandas as pd
import numpy as np
from datetime import datetime, timedelta

tabela_fundo = pd.read_csv("tbl_fundos.csv")
tabela_cota = pd.read_csv("tbl_cotas.csv")
tabela_indicadores = pd.read_csv("tbl_indicadores.csv")

print(tabela_fundo.head())
print(tabela_fundo.shape)
tabela_fundo.info()
print(tabela_fundo.isnull().sum())
print(tabela_fundo.duplicated().sum())

print(tabela_fundo['nome_fundo'].unique())

tabela_fundo['nome_fundo'] = tabela_fundo['nome_fundo'].str.strip()

tabela_fundo.loc[tabela_fundo['nome_fundo'].str.contains("nan", case=False, na=False), 'nome_fundo'] = np.nan
tabela_fundo.loc[~tabela_fundo['nome_fundo'].str.contains(r"Fundo\s[a-zA-Z]", case=False, na=False), 'nome_fundo'] = np.nan
tabela_fundo['nome_fundo'] = tabela_fundo['nome_fundo'].fillna('Desconhecido').str.title()

print(tabela_fundo['nome_fundo'].unique())
print(tabela_fundo['nome_fundo'])


print(tabela_fundo['categoria'])
print(tabela_fundo['categoria'].unique())
print(tabela_fundo['categoria'].isnull().sum())

categorias = {

    'Acoes' : 'Ações',
    'Ação' : 'Ações',
    'Ações' : 'Ações',
    'RF' : 'Renda Fixa',
    'Renda Fixa' : 'Renda Fixa',
    'Multi' : 'Multimercado',
    'Multimercado' : 'Multimercado',
    'Previdenciário' : 'Previdenciário'

}

tabela_fundo['categoria'] = tabela_fundo['categoria'].map(categorias).astype('string')

tabela_fundo['categoria'] = tabela_fundo['categoria'].fillna('Outros')

print(tabela_fundo['categoria'])
print(tabela_fundo['categoria'].unique())
print(tabela_fundo['categoria'].isnull().sum())

print(tabela_fundo['data_inicio'])
print(tabela_fundo['data_inicio'].isnull().sum())

tabela_fundo['data_inicio'] = tabela_fundo['data_inicio'].str.replace("/", "-")
tabela_fundo['data_inicio'] = tabela_fundo['data_inicio'].str.replace(r"(\d{2})-(\d{2})-(\d{4})", r"\3-\2-\1", regex=True)
tabela_fundo['data_inicio'] = pd.to_datetime(tabela_fundo['data_inicio'], errors='coerce')

print(tabela_fundo['data_inicio'])
print(tabela_fundo['data_inicio'].isnull().sum())
print(tabela_fundo[tabela_fundo['data_inicio'].dt.year > 2026])

print(tabela_fundo['patrimonio_inicial'])
print(tabela_fundo['patrimonio_inicial'].unique())
print(tabela_fundo['patrimonio_inicial'].isnull().sum())

tabela_fundo['patrimonio_inicial'] = tabela_fundo['patrimonio_inicial'].str.replace(",", ".")
tabela_fundo['patrimonio_inicial'] = tabela_fundo['patrimonio_inicial'].str.replace(r"(.*)(\.)(\d+)", r"\1,\3", regex=True)
tabela_fundo['patrimonio_inicial'] = tabela_fundo['patrimonio_inicial'].str.replace(r"\.", "", regex=True)
tabela_fundo['patrimonio_inicial'] = tabela_fundo['patrimonio_inicial'].str.replace(",", ".").astype(float)

print(tabela_fundo['patrimonio_inicial'])
print(tabela_fundo['patrimonio_inicial'].unique())
print(tabela_fundo['patrimonio_inicial'].isnull().sum())

print(tabela_fundo['taxa_administracao'])
print(tabela_fundo['taxa_administracao'].unique())

tabela_fundo['taxa_administracao'] = tabela_fundo['taxa_administracao'].str.replace("%", '').astype(float)

print(tabela_fundo['taxa_administracao'])
print(tabela_fundo['taxa_administracao'].unique())

print(tabela_fundo.head())
print(tabela_fundo.shape)
tabela_fundo.info()
print(tabela_fundo.describe())
print(tabela_fundo.isnull().sum())

#Parte dois

print(tabela_cota.head())
print(tabela_cota.shape)
tabela_cota.info()
print(tabela_cota.isnull().sum())

tabela_cota = tabela_cota[tabela_cota['id_fundo'].isin(tabela_fundo['id_fundo'])]

print(tabela_cota['data_cota'])

tabela_cota['data_cota'] = tabela_cota['data_cota'].str.replace("/", "-")
tabela_cota['data_cota'] = tabela_cota['data_cota'].str.replace(r"(\d{2})-(\d{2})-(\d{4})", r"\3-\2-\1", regex=True)
tabela_cota['data_cota'] = pd.to_datetime(tabela_cota['data_cota'], errors='coerce')

print(tabela_cota['data_cota'])
print(tabela_cota[tabela_cota['data_cota'].dt.year > 2026])

print(tabela_cota['cotacao'])
print(tabela_cota['cotacao'].unique())

tabela_cota['cotacao'] = tabela_cota['cotacao'].round(2)

print(tabela_cota['cotacao'])
print(tabela_cota['cotacao'].unique())

print(tabela_cota['rentabilidade_dia'])

tabela_cota['rentabilidade_dia'] = tabela_cota['rentabilidade_dia'].round(3)

print(tabela_cota['rentabilidade_dia'])

print(tabela_cota['volume_negociado'])
print(tabela_cota[tabela_cota['volume_negociado'] < 0])

tabela_cota['volume_negociado'] = tabela_cota['volume_negociado'].abs()

print(tabela_cota['cotacao'])
print(tabela_cota[tabela_cota['volume_negociado'] < 0])

print(tabela_cota.head())
print(tabela_cota.shape)
tabela_cota.info()
print(tabela_cota.isnull().sum())

#Parte três

print(tabela_indicadores.head())
print(tabela_indicadores.shape)
tabela_indicadores.info()
print(tabela_indicadores.isnull().sum())

print(tabela_indicadores['data'])



#print(tabela_indicadores['cdi'])
#print(tabela_indicadores['ibovespa'])
#print(tabela_indicadores['volatilidade'])