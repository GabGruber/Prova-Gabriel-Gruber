import numpy as np

S1 = 70
S2 = 50
payoff = 60
T = 0.5
r = 13
sigma1 = 30
sigma2 = 20
rho = 37
barreira_low = 55
barreira_high = 65
num_simulations = 1000

# Convertendo taxas para unidades adequadas
r = r / 100
sigma1 = sigma1 / 100
sigma2 = sigma2 / 100
rho = rho /100

# Criando arrays
S1_barriera = np.array([barreira_low, barreira_high])
S2_barriera = np.array([barreira_low, barreira_high])

# Criando a Matriz de covariancia dos retornos dos ativos
cov_matriz = np.array([[sigma1 ** 2, rho * sigma1 * sigma2], [rho * sigma1 * sigma2, sigma2 ** 2]])

# Calculando Matriz de Cholesky pois as variáveis podem ser dependentes
Chol = np.linalg.cholesky(cov_matriz)

# Definindo parâmetros de MC
dt = T / 365
num_steps = int(T / dt)

# Criando Matrizes vazias para armazenar os preços simulados
S1_matriz_preco = np.zeros((num_simulations, num_steps + 1))
S2_matriz_preco = np.zeros((num_simulations, num_steps + 1))
S1_matriz_preco[:, 0] = S1
S2_matriz_preco[:, 0] = S2

# Simula os preços dos ativos subjacentes
for i in range(num_simulations):
    for j in range(1, num_steps + 1):
        # Gera números aleatórios normais independentes
        Z1 = np.random.normal()
        Z2 = np.random.normal()
        # Gera números aleatórios normais correlacionados
        X1, X2 = np.dot(Chol, [Z1, Z2])
        # Calcula o próximo preço do ativo S1
        S1_matriz_preco[i, j] = S1_matriz_preco[i, j - 1] * np.exp(
            (r - 0.5 * sigma1 ** 2) * dt + sigma1 * np.sqrt(dt) * X1)
        # Calcula o próximo preço do ativo S2
        S2_matriz_preco[i, j] = S2_matriz_preco[i, j - 1] * np.exp(
            (r - 0.5 * sigma2 ** 2) * dt + sigma2 * np.sqrt(dt) * X2)

# Calcula quantas vezes cada ativo ficou no intervalo
S1_touches_barrier = np.logical_and(np.min(S1_matriz_preco[:, 1:], axis=1) >= barreira_low,
                                    np.max(S1_matriz_preco[:, 1:], axis=1) <= barreira_high)
S2_touches_barrier = np.logical_and(np.min(S2_matriz_preco[:, 1:], axis=1) >= barreira_low,
                                    np.max(S2_matriz_preco[:, 1:], axis=1) <= barreira_high)

# Quantas vezes ambos os ativos ficaram no intervalo simultaneamente
num_touches = np.sum(np.logical_and(S1_touches_barrier, S2_touches_barrier))

# Array dos Payoffs
payoffs = np.where(num_touches > 0, payoff, 0)

# Cálculo do valor da opção
option_price = np.exp(-r * T) * payoffs.mean()

