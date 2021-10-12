import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.stats import ttest_ind
from sklearn.metrics import r2_score


def mat(n):
    mat_file = loadmat('zadanie_1i2_zbior_' + str(n) + '.mat')
    data = mat_file['dane' + str(n)]
    uu = data[:, 0]
    yy = data[:, 1]

    return uu, yy


def predict(u, y, th):
    y_pred = th[1] * u + th[0]
    Q = np.sum((y - y_pred) ** 2)

    return y_pred, Q


def gradient_descent(u, y, theta, max_epochs, l_rate):
    df = np.zeros(2)

    for i in range(max_epochs):
        y_pred, Q = predict(u, y, theta)

        df[1] = -2 * np.sum(u * (y - y_pred))
        df[0] = -2 * np.sum(y - y_pred)
        theta[1] -= l_rate * df[1]
        theta[0] -= l_rate * df[0]
    y_pred, Q = predict(u, y, theta)

    return theta, y_pred, Q


U, Y = mat(1)
theta_init = np.array([1.0, 1.0])
epochs = 10000
alpha = 0.00001

Theta, Y_pred, Q = gradient_descent(U, Y, theta_init, epochs, alpha)
R2 = r2_score(Y, Y_pred)
tstud = ttest_ind(Y, Y_pred)

print('Model parameters:', Theta)
print('R^2:', R2)
print('t-statistic:', tstud)
plt.scatter(U, Y, label='real')
plt.scatter(U, Y_pred, label='predicted')
plt.title('Gradient descent (l_rate = {}, {} epochs)  Q = {:.2f}'.format(alpha, epochs, Q))
plt.xlabel('u')
plt.ylabel('y')
plt.legend()
plt.show()
