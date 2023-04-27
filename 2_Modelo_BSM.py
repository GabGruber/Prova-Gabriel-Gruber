import numpy as np
from datetime import date
from scipy.stats import norm

def black_scholes(S, K, r, T, sigma, option_type):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if tipo == 'CALL':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif tipo == 'PUT':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price


S = float(input("Preço atual do ativo subjacente: "))
K = float(input("Preço de exercício da opção: "))
r = float(input("Taxa livre de risco anual (%): ")) / 100
T = (input("Tempo restante até o vencimento da opção (em anos) ou a data do vencimento (DD/MM/YYYY)"))
if isinstance(T, date):
    hoje = datetime.now().date()
    dias_ate_vencimento = (data_vencimento - hoje).days
    dias_ate_vencimento = dias_ate_vencimento/365
else:
    T = float(T)

sigma = float(input("Volatilidade do ativo (%): ")) / 100
tipo = input("Tipo de opção (CALL ou PUT): ")
tipo = tipo.upper()
if tipo not in ["CALL","PUT"]:
    print("Favor inputar o tipo da opção novamente (call ou put)")
    exit()

option_price = black_scholes(S, K, r, T, sigma, tipo)
print("Preço da opção: ", option_price)