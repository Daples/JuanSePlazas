import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import statsmodels.tsa.arima.model as sm

plt.rc('text', usetex=True)
plt.rcParams.update({'font.size': 16})

def simulateARMA11(x0, T, beta, sigma2=1):
    xs = np.zeros(T+1)
    xs[0] = x0
    ts = np.linspace(0, T+1, T+1)
    e = st.norm.rvs(size=xs.shape, scale=sigma2)
    for t in range(1, T+1):
        xs[t] = beta[0]*xs[t-1] + e[t] - beta[1]*e[t-1]
    return ts, xs


# method -> 1 : Uses numerical approximation of derivative.
#        -> 2 : Uses exact derivative (iterative calculation).
# cond   -> 0 : Uses non-conditional estimation.
#        -> 1 : Uses conditional estimation.
def fit_ARMA11(xs, beta0, tol=1e-7, h=1e-7, method=1, cond=True):
    def estimate_epsilon(xs, beta):
        e = np.zeros((xs.size, 1))
        for t in range(1, xs.size):
            e[t] = xs[t] - beta[0]*xs[t-1] + beta[1]*e[t-1]
        return e

    def exact_derivative(xs, e, beta):
        d = np.zeros((xs.size, 1))
        for t in range(1, xs.size):
            d[t] = beta[1]*d[t-1] + e[t-1]
        return d

    def estimate_epsilon_noncond(xs, beta, n_iter=100, tol=1e-7):
        etas = [xs[-1]]
        T = xs.size
        for T0 in range(T-1, 0, -1):
            etas.append(xs[T0] - beta[0, 0]*xs[T0-1] + beta[1, 0]*etas[-1])

        ws = [beta[0, 0]*xs[0] - beta[1, 0]*etas[-1]]
        k = 0
        while k <= n_iter:
            ws.append(beta[0, 0]*ws[-1])
            if ws[-1] <= tol:
                break

        xs_ext = np.hstack((np.array(ws), xs))
        e = estimate_epsilon(xs_ext, beta)
        return e[-(T+1):], ws[0]

    if cond:
        T = xs.size - 1
    else:
        T = xs.size
    beta = np.array(beta0).reshape(2, 1)
    Z = np.zeros((T, 2))
    k = 0
    norms = []
    while True:
        if cond:
            ek = estimate_epsilon(xs, beta)
            Z[:, 0] = xs[:-1]
            xs0 = xs
        else:
            ek, w0 = estimate_epsilon_noncond(xs, beta)
            xs0 = np.hstack((w0, xs))
            Z[:, 0] = xs0[:-1]
        if method == 1:
            aux = np.array([[0], [h]])
            ekh = estimate_epsilon(xs0, beta + aux)
            Z[:, 1] = -(ekh[1:, 0] - ek[1:, 0])/h
        elif method == 2:
            derivative = exact_derivative(xs0, ek, beta)
            Z[:, 1] = -derivative[1:, 0]
        estimated_diff = np.linalg.inv(Z.T.dot(Z)).dot(Z.T).dot(ek[1:])
        new_beta = beta + estimated_diff
        norms.append(np.linalg.norm(beta - new_beta, ord=np.Inf))
        if norms[-1] < tol:
            break
        beta = new_beta
        k += 1
    return new_beta, norms


# Test for ARMA(1,1) - beta = [[0.3], [-0.5]]
# Conditional
ts, xs = simulateARMA11(0, 1000, [0.3, -0.5])
beta_cond, norms_cond = fit_ARMA11(xs, [0.5, -0.3], method=1, cond=True)
print('beta_cond', beta_cond[0], beta_cond[1])
#
# # Non-conditional
# beta, norms = fit_ARMA11(xs, [0.5, -0.3], method=2, cond=False)
# print('beta', beta[0], beta[1])
# plt.plot(norms, 'k')
# plt.xlabel('$k$')
# plt.ylabel('$||\\beta^{k+1}-\\beta^k||_\infty$')
# plt.savefig('test.pdf', bbox_inches='tight')
# plt.clf()

################################################
# Data from last assignment
# Read data
# file = open('seguimiento5.csv', 'r')
# file = file.read().split('\n')[1:-1]
# data = np.array([line.split(',')[1] for line in file], dtype=float)
#
# # Estimate ARMA(1,1)
# beta, norms = fit_ARMA11(data[:100], [0.4, -0.2], method=2, cond=False)
# plt.plot(norms, 'k')
# plt.xlabel('$k$')
# plt.ylabel('$||\\beta^{k+1}-\\beta^k||_\infty$')
# plt.savefig('data.pdf', bbox_inches='tight')
# plt.clf()
# print('My beta', beta[0], beta[1])
# mod = sm.ARIMA(data, order=(1, 0, 1))
# res = mod.fit()
# print('Statsmodels beta', res.arparams, -res.maparams)
# print(res.summary())
