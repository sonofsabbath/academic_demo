import numpy as np
import matplotlib.pyplot as plt


def gbm(dt, x0, mi, sigma, n=1000):
    """Wyznacza n punktów trajektorii geometrycznego ruchu Browna o przyroście dt, punkcie początkowym x0, dryfie mi
        oraz zmienności sigma"""

    db = np.random.normal(size=n-1)  # próbki z rozkładu normalnego (n - 1, bo mamy już wartość w x(0))
    y = np.zeros(n)  # dla ułatwienia inicjujemy wektor wypełniony zerami
    y[0] = x0

    for i in range(1, n):
        y[i] = y[i - 1] * np.exp((mi - (sigma ** 2 / 2)) * dt + sigma * np.sqrt(dt) * db[i - 1])

    return y


def deterministic_brown(dt, x0, mi, n=1000):
    """Wyznacza n punktów trajektorii deterministycznego trendu o przyroście dt, punkcie początkowym x0 i dryfie mi"""
    y = np.zeros(n)
    y[0] = x0

    for i in range(1, n):
        y[i] = y[i - 1] * np.exp(mi * dt)

    return y


def draw(y1, y2, y3, y_det):
    """Rysuje trajektorie y1, y2 i y3 oraz deterministyczny trend y_det"""

    plt.plot(y1)
    plt.plot(y2, color='green')
    plt.plot(y3, color='red')
    plt.plot(y_det, color='black', label='Deterministic')
    plt.legend()
    plt.title('GBM')
    plt.show()


brown_1 = gbm(1, 10, 0.01, 0.04)
brown_2 = gbm(1, 10, 0.01, 0.04)
brown_3 = gbm(1, 10, 0.01, 0.04)
brown_deter = deterministic_brown(1, 10, 0.01)
draw(brown_1, brown_2, brown_3, brown_deter)
