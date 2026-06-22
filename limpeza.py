import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Lendo as tabelas e transformando elas em DataFrames
tabela_fundo = pd.read_csv("tbl_fundos.csv")
tabela_cota = pd.read_csv("tbl_cotas.csv")
tabela_indicadores = pd.read_csv("tbl_indicadores.csv")

# ===== Primeira Tabela (tabela_fundo) =====

# Analisando a tabela e o que tem dentro dela para limpar
print(tabela_fundo.head()) # Analisando a estrutura inicial da tabela e seus registros
print(tabela_fundo.shape) # Vendo a quantidade de colunas/linhas para controle de volumetria posterior
tabela_fundo.info() # Verificando os tipos primitivos das colunas (dtypes)
print(tabela_fundo.isnull().sum()) # Analisando a quantidade de valores nulos pendentes de tratamento
print(tabela_fundo.duplicated().sum()) # Vendo se tem linhas duplicadas na base cadastral (Não tem!)

# ===== Limpando a coluna 'nome_fundo' ======

print(tabela_fundo['nome_fundo'].head()) # Analisando os primeiros registros textuais da coluna
print(tabela_fundo['nome_fundo'].unique()) # Mapeando todos os nomes únicos para caçar anomalias e padrões de sujeira

tabela_fundo['nome_fundo'] = tabela_fundo['nome_fundo'].str.strip() # Tirando os espaços vazios no início e fim das strings

tabela_fundo.loc[tabela_fundo['nome_fundo'].str.contains("nan", case=False, na=False), 'nome_fundo'] = np.nan # Identificando strings textuais 'nan' e convertendo em nulo real (NaN)
tabela_fundo.loc[~tabela_fundo['nome_fundo'].str.contains(r"Fundo\s[a-zA-Z]", case=False, na=False), 'nome_fundo'] = np.nan # Filtro RegEx: invalida e transforma em nulo tudo que não seguir a estrutura padrão "Fundo [Letra]"
tabela_fundo['nome_fundo'] = tabela_fundo['nome_fundo'].fillna('Desconhecido').str.title() # Preenche os nulos criados e padroniza os nomes válidos com a primeira letra maiúscula

print(tabela_fundo['nome_fundo'].unique()) # Analisando se o tratamento funcionou e limpou as anomalias textuais
print(tabela_fundo['nome_fundo']) # Conferindo o resultado final da coluna de nomes

# ===== Limpando a coluna 'categoria' =====

print(tabela_fundo['categoria']) # Analisando os registros de categorias da base
print(tabela_fundo['categoria'].unique()) # Mapeando as variações textuais escritas de forma errada ou desalinhada
print(tabela_fundo['categoria'].isnull().sum()) # Analisando se existem valores nulos de fábrica nesta coluna

categorias = {
    'Acoes' : 'Ações',
    'Ação' : 'Ações',
    'Ações' : 'Ações',
    'RF' : 'Renda Fixa',
    'Renda Fixa' : 'Renda Fixa',
    'Multi' : 'Multimercado',
    'Multimercado' : 'Multimercado',
    'Previdenciário' : 'Previdenciário'
} # Criando um dicionário de de-para para mapear e unificar todas as variações na grafia correta

tabela_fundo['categoria'] = tabela_fundo['categoria'].map(categorias).astype('string') # Aplicando o mapeamento de padronização e forçando o tipo para string do Pandas

tabela_fundo['categoria'] = tabela_fundo['categoria'].fillna('Outros') # Tratando valores não mapeados ou originalmente nulos como a categoria genérica 'Outros'

print(tabela_fundo['categoria']) # Conferindo o alinhamento da coluna na tela
print(tabela_fundo['categoria'].unique()) # Validando se restaram categorias fora do padrão esperado
print(tabela_fundo['categoria'].isnull().sum()) # Vendo se restaram valores nulos (Não tem!)

# ===== Limpando a coluna 'data_inicio' =====

print(tabela_fundo['data_inicio']) # Verificando a formatação original das strings de data de início dos fundos
print(tabela_fundo['data_inicio'].isnull().sum()) # Verificando a volumetria de nulos nesta coluna

tabela_fundo['data_inicio'] = tabela_fundo['data_inicio'].str.replace("/", "-") # Substituindo barras por hífens para iniciar a padronização textual
tabela_fundo['data_inicio'] = tabela_fundo['data_inicio'].str.replace(r"(\d{2})-(\d{2})-(\d{4})", r"\3-\2-\1", regex=True) # RegEx com grupos de captura para inverter o formato brasileiro (DD-MM-AAAA) para o formato internacional (AAAA-MM-DD)
tabela_fundo['data_inicio'] = pd.to_datetime(tabela_fundo['data_inicio'], errors='coerce') # Convertendo para o tipo datetime real do Pandas, transformando datas inválidas/bizarras em NaT/NaN de forma segura

print(tabela_fundo['data_inicio']) # Visualizando a coluna de data devidamente tipada e convertida
print(tabela_fundo['data_inicio'].isnull().sum()) # Analisando se sobrou algum valor nulo após a conversão
print(tabela_fundo[tabela_fundo['data_inicio'].dt.year > 2026]) # Validação de consistência de negócio: caçando fundos criados no futuro (maiores que o ano atual de 2026) (Não tem!)

# ===== Limpando a coluna 'patrimonio_inicial' =====

print(tabela_fundo['patrimonio_inicial']) # Analisando o padrão de numeração (provável formato de texto com separadores brasileiros)
print(tabela_fundo['patrimonio_inicial'].unique()) # Avaliando a distribuição visual dos registros
print(tabela_fundo['patrimonio_inicial'].isnull().sum()) # Mapeando nulos na coluna de patrimônio

tabela_fundo['patrimonio_inicial'] = tabela_fundo['patrimonio_inicial'].str.replace(",", ".") # Forçando a troca de vírgulas por pontos para iniciar a Engenharia de reversão de formato
tabela_fundo['patrimonio_inicial'] = tabela_fundo['patrimonio_inicial'].str.replace(r"(.*)(\.)(\d+)", r"\1,\3", regex=True) # RegEx para capturar as casas decimais reais e isolá-las com uma vírgula temporária
tabela_fundo['patrimonio_inicial'] = tabela_fundo['patrimonio_inicial'].str.replace(r"\.", "", regex=True) # Removendo os pontos que representavam separadores de milhar originais
tabela_fundo['patrimonio_inicial'] = tabela_fundo['patrimonio_inicial'].str.replace(",", ".").astype(float) # Trocando a vírgula decimal temporária por ponto e forçando a conversão para float64

print(tabela_fundo['patrimonio_inicial']) # Conferindo o comportamento dos floats criados (incluindo a manutenção correta de patrimônios negativos)
print(tabela_fundo['patrimonio_inicial'].unique()) # Verificando a distribuição dos números puros limpos
print(tabela_fundo['patrimonio_inicial'].isnull().sum()) # Analisando se sobrou algum valor nulo ou erro de conversão (Não tem!)

# ===== Limpando a coluna 'taxa_administracao' =====

print(tabela_fundo['taxa_administracao']) # Inspecionando o padrão da taxa (provável texto contendo o caractere '%')
print(tabela_fundo['taxa_administracao'].unique()) # Mapeando as taxas exclusivas registradas

tabela_fundo['taxa_administracao'] = tabela_fundo['taxa_administracao'].str.replace("%", '').astype(float) # Expurgando o símbolo de porcentagem e convertendo a string diretamente para tipo numérico float

print(tabela_fundo['taxa_administracao']) # Conferindo o resultado na tela (exibindo formato numérico float do Python)
print(tabela_fundo['taxa_administracao'].unique()) # Validando se os valores numéricos únicos estão corretos e consistentes

# Check de encerramento da Primeira Tabela
print(tabela_fundo.head()) # Visualizando o DataFrame cadastral totalmente limpo e tratado
print(tabela_fundo.shape) # Validando que o número original de colunas e linhas foi controlado com sucesso
tabela_fundo.info() # Confirmando que todas as colunas agora possuem dtypes ideais para análise (strings, datetime e floats)
print(tabela_fundo.describe()) # Aplicando estatística descritiva para uma primeira varredura visual de possíveis anomalias
print(tabela_fundo.isnull().sum()) # Verificação final de nulos da primeira tabela

# ===== Segunda Tabela (tabela_cota) =====

print(tabela_cota.head()) # Analisando o cabeçalho e a estrutura da série histórica de cotas
print(tabela_cota.shape) # Mapeando a volumetria de registros de cotações da base
tabela_cota.info() # Verificando os tipos de dados originais fornecidos
print(tabela_cota.isnull().sum()) # Analisando a presença de nulos na tabela de cotações
print(tabela_cota.duplicated().sum()) # Caçando duplicatas na série temporal (Não tem!)

tabela_cota = tabela_cota[tabela_cota['id_fundo'].isin(tabela_fundo['id_fundo'])] # Integridade Referencial: filtrando e mantendo na base apenas cotas de IDs que existem na tabela de fundos cadastrados

print(tabela_cota['data_cota']) # Analisando a formatação textual das datas das cotações

tabela_cota['data_cota'] = tabela_cota['data_cota'].str.replace("/", "-") # Substituindo barras por hífens para padronização temporal
tabela_cota['data_cota'] = tabela_cota['data_cota'].str.replace(r"(\d{2})-(\d{2})-(\d{4})", r"\3-\2-\1", regex=True) # RegEx para converter o formato de texto brasileiro para o padrão internacional (AAAA-MM-DD)
tabela_cota['data_cota'] = pd.to_datetime(tabela_cota['data_cota'], errors='coerce') # Convertendo para tipo datetime do Pandas e transformando registros corrompidos em nulos de forma assistida

print(tabela_cota['data_cota']) # Conferindo a coluna temporal limpa e tipada
print(tabela_cota[tabela_cota['data_cota'].dt.year > 2026]) # Checando se existem registros incoerentes com datas no futuro (Não tem!)

# ===== Limpando a coluna 'cotacao' =====

print(tabela_cota['cotacao']) # Analisando a precisão decimal original da coluna de cotações
print(tabela_cota['cotacao'].unique()) # Verificando a distribuição de precisão dos valores

tabela_cota['cotacao'] = tabela_cota['cotacao'].round(2) # Arredondando o valor numérico float para duas casas decimais, limpando o ruído visual de frações de centavos da base original

print(tabela_cota['cotacao']) # Conferindo o resultado do arredondamento na tela
print(tabela_cota['cotacao'].unique()) # Validando que o padrão numérico de 2 casas foi aplicado uniformemente

# ===== Limpando a coluna 'rentabilidade_dia' =====

print(tabela_cota['rentabilidade_dia']) # Inspecionando os valores decimais da rentabilidade diária

tabela_cota['rentabilidade_dia'] = tabela_cota['rentabilidade_dia'].round(3) # Arredondando para 3 casas decimais, mantendo a sensibilidade padrão de mercado para variações percentuais em fundos

print(tabela_cota['rentabilidade_dia']) # Conferindo o resultado do ajuste

# ===== Limpando a coluna 'volume_negociado' =====

print(tabela_cota['volume_negociado']) # Analisando o comportamento original do volume financeiro movimentado por dia
print(tabela_cota[tabela_cota['volume_negociado'] < 0]) # Mapeando registros incoerentes abaixo de zero (volumes não podem ser negativos no mercado)

tabela_cota['volume_negociado'] = tabela_cota['volume_negociado'].abs() # Correção de sinal: aplicando a função absoluta na própria coluna de volume para converter valores negativos em positivos

print(tabela_cota['cotacao']) # Garantindo em tela que os valores da coluna de cotação não foram alterados acidentalmente
print(tabela_cota[tabela_cota['volume_negociado'] < 0]) # Sanity Check: validando que o filtro limpou com sucesso todos os volumes negativos

# Check de encerramento da Segunda Tabela
print(tabela_cota.head()) # Visualizando a tabela de cotações totalmente tratada
print(tabela_cota.shape) # Checando as dimensões finais da tabela após os filtros de integridade referencial
tabela_cota.info() # Conferindo se a tipagem da tabela de cotas está 100% correta
print(tabela_cota.isnull().sum()) # Confirmação final de ausência de nulos inesperados na segunda tabela

# ===== Terceira Tabela (tabela_indicadores) =====

print(tabela_indicadores.head()) # Analisando os primeiros registros dos indicadores de mercado
print(tabela_indicadores.shape) # Mapeando a volumetria da base de índices
tabela_indicadores.info() # Analisando os tipos primitivos originais antes do início do processo de limpeza
print(tabela_indicadores.isnull().sum()) # Mapeando a quantidade de nulos originais por coluna

# ===== Limpando a coluna 'data' =====

print(tabela_indicadores['data']) # Verificando a estrutura de texto das datas macroeconômicas

tabela_indicadores['data'] = tabela_indicadores['data'].str.replace(r"(\d{2})-(\d{2})-(\d{4})", r"\3-\2-\1", regex=True) # RegEx para inverter a string da data para o padrão internacional ISO (AAAA-MM-DD)
tabela_indicadores['data'] = pd.to_datetime(tabela_indicadores['data'], errors='coerce') # Convertendo a string para tipo datetime nativo do Pandas de forma resiliente

print(tabela_indicadores['data']) # Conferindo a exibição do novo campo de data tipado
print(tabela_indicadores[tabela_indicadores['data'].dt.year > 2026]) # Garantindo que não existem distorções com anos no futuro superiores a 2026

# ===== Limpando a coluna 'cdi' =====

print(tabela_indicadores['cdi']) # Inspecionando a taxa de juros CDI (provável string com padrão de pontuação brasileiro)

tabela_indicadores['cdi'] = tabela_indicadores['cdi'].str.replace(",", ".") # Substituindo a vírgula decimal brasileira por ponto para adequação ao Python
tabela_indicadores['cdi'] = tabela_indicadores['cdi'].astype(float) # Modificando a coluna para float64, permitindo cálculos e comparativos matemáticos posteriores

print(tabela_indicadores['cdi']) # Conferindo os valores decimais limpos do CDI
print(tabela_indicadores['cdi'].unique()) # Verificando a distribuição de taxas únicas pós-conversão

# ===== Limpando a coluna 'ibovespa' =====

print(tabela_indicadores['ibovespa']) # Inspecionando a formatação textual da pontuação do índice Ibovespa
print(tabela_indicadores['ibovespa'].unique()) # Mapeando os registros únicos para verificar o padrão de caracteres

tabela_indicadores['ibovespa'] = tabela_indicadores['ibovespa'].str.replace(",", ".") # Substituindo a vírgula por ponto para alinhar a casa decimal do índice
tabela_indicadores['ibovespa'] = tabela_indicadores['ibovespa'].astype(float) # Convertendo o Ibovespa de texto para float64 para viabilizar cálculos de rentabilidade acumulada e correlações

print(tabela_indicadores['ibovespa']) # Confirmando o sucesso da conversão da pontuação em float puro
print(tabela_indicadores['ibovespa'].unique()) # Verificando a consistência dos registros limpos do índice

# ===== Limpando a coluna 'volatilidade' =====

print(tabela_indicadores['volatilidade']) # Inspecionando a coluna de volatilidade macroeconômica
print(tabela_indicadores['volatilidade'].unique()) # Confirmando em tela que os registros já vieram puramente numéricos e livres de caracteres como '%'

# Check de encerramento da Terceira Tabela
print(tabela_indicadores.head()) # Checando a tabela de indicadores com todas as alterações consolidadas
print(tabela_indicadores.shape) # Validando se o formato e tamanho da estrutura de índices macroeconômicos foram mantidos
tabela_indicadores.info() # Conferindo se todas as colunas de índices agora são 'float64' e a data é 'datetime64'
print(tabela_indicadores.isnull().sum()) # Confirmação de fechamento de nulos da terceira tabela

# ===== Modelagem de Dados e Unificação (Merge) =====

# Realizando um Left Join para correlacionar e unificar os metadados cadastrais dos fundos com as séries temporais diárias das cotações usando o 'id_fundo' como chave estrangeira
tabela_final = pd.merge(tabela_fundo, tabela_cota, on='id_fundo', how='left')
print(tabela_final.isnull().sum()) # Analisando nulos pós-cruzamento para capturar fundos ativos no cadastro que nunca geraram dados históricos de cotação

# ===== Salvando as tabelas finais (Carga do pipeline de ETL) =====

tabela_final.to_csv("tbl_final_limpo.csv", index=False) # Exportando o Dataframe unificado final limpo de índices para alimentar a camada de análise/outliers
tabela_indicadores.to_csv("tbl_indicadores_limpo.csv", index=False) # Exportando a tabela de indicadores macroeconômicos higienizada

# Vendo se funcionou
print("Tabelas salvas com sucesso!") # Confirmação final impressa no terminal indicando o término com sucesso de todo o ecossistema de ETL