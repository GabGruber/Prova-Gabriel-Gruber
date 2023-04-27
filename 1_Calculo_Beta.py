import pandas as pd

filepath = 'C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\mkt_returns.txt'

data = pd.read_csv(filepath, index_col='Date')

# Calcula os retornos diários
returns = data.pct_change()

# Seleciona as colunas de ações
stock_returns = returns.drop('SPY', axis=1)

# Seleciona a coluna com o SPY
index_returns = returns['SPY']

# Calcula a covariância entre as ações e o índice
cov_returns = returns.cov()
cov_returns = cov_returns[['SPY']]

# Calcula a variância do índice
market_variance = index_returns.var()

# Calcula o beta para cada ação
beta = cov_returns / market_variance

# Exibe os resultados
print(beta)