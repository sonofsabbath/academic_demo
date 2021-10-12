import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.io import loadmat
from scipy.stats import ttest_ind


def mat(n):
    mat_file = loadmat('zadanie_1i2_zbior_' + str(n) + '.mat')
    data = mat_file['dane' + str(n)]
    uu = data[:, 0]
    yy = data[:, 1]

    return uu.reshape((-1, 1)), yy


u, y = mat(1)
model = LinearRegression(fit_intercept=True)
model.fit(u, y)
y_pred = model.predict(u)

R2 = model.score(u, y)
Q = np.sum((y - y_pred) ** 2)
tstud = ttest_ind(y, y_pred)

print('Model parameters:', model.intercept_, model.coef_)
print('R^2:', R2)
print('t-statistic:', tstud)
plt.scatter(u, y, label='real')
plt.scatter(u, y_pred, label='predicted')
plt.title('Least squares method  Q = {:.2f}'.format(Q))
plt.xlabel('u')
plt.ylabel('y')
plt.legend()
plt.show()
