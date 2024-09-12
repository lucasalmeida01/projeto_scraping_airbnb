import pandas as pd
import sqlite3
from datetime import datetime

# Setando o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# Criando o df
df = pd.read_json("E:\projeto_scraping_chaves_na_mao\src\data\imoveis.jsonl", lines=True)

# Dados sem formatação
print(df.head())


# alterando o tipo de dados para int e alterando valores nulos para 0 
df['quartos']  = df['quartos'].fillna(0).astype(int)
df['banheiros'] = df['banheiros'].fillna(0).astype(int)
df['garagens'] = df['garagens'].fillna(0).astype(int)

# Queremos usar a formatação de milhares (f'{x:,.0f}') e para isso precisamos do valor em string

# Vamos manter as colunas "alguel" e "condominio" como string, removendo caracteres indesejados, substituindo ponto por nada e virgula por ponto, removendo espaços em branco 
# Para a coluna "condominio" vamos preencher nulos com 0
df['aluguel'] = df['aluguel'].str.replace('R$', '').str.replace('.', '').replace(',', '.').str.strip()
df['condominio'] = df['condominio'].str.replace('R$', '').str.replace('Cond.:', '').replace('.', '').replace(',', '.').str.strip().fillna('0')

# A coluna "aluguel_total" é a soma do aluguel com condominio, para calculo precisamos dos valores em float 
df['aluguel_total'] = df['aluguel'].str.replace('.', '').astype(float) + df['condominio'].str.replace('.', '').astype(float)

# Convertendo todas as colunas para o formato de exibição com separadores de milhares
df['aluguel'] = df['aluguel'].apply(lambda x: f'{float(x):,.0f}'.replace(',', '.'))
df['condominio'] = df['condominio'].apply(lambda x: f'{float(x):,.0f}'.replace(',', '.'))
df['aluguel_total'] = df['aluguel_total'].apply(lambda x: f'{x:,.0f}'.replace(',', '.'))


# Exibindo o dataframe no formato desejado
print(df.head())

print(df.info())

# verificando quantidade de registros
print(df.count())

#1257 registros
print(len(df))