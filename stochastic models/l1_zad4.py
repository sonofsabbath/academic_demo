import numpy as np
import matplotlib.pyplot as plt


def abm(dt, x0, mi, sigma, n=1000):
    """Wyznacza n punktów trajektorii arytmetycznego ruchu Browna o przyroście dt, punkcie początkowym x0, dryfie mi
        oraz zmienności sigma"""

    db = np.random.normal(0, dt, n - 1)  # próbki z rozkładu normalnego (n - 1, bo mamy już wartość w x(0))
    y = np.zeros(n)  # dla ułatwienia inicjujemy wektor wypełniony zerami
    y[0] = x0

    for i in range(1, n):
        y[i] = y[i - 1] + mi * dt + sigma * db[i - 1]  # db[i - 1], bo n - 1 próbek

    return y


def deterministic_brown(dt, x0, mi, n=1000):
    """Wyznacza n punktów trajektorii deterministycznego trendu o przyroście dt, punkcie początkowym x0 i dryfie mi"""
    y = np.zeros(n)
    y[0] = x0

    for i in range(1, n):
        y[i] = y[i - 1] + mi * dt

    return y


def draw(y1, y2, y3, y_det):
    """Rysuje trajektorie y1, y2 i y3 oraz deterministyczny trend y_det"""

    plt.plot(y1)
    plt.plot(y2, color='green')
    plt.plot(y3, color='red')
    plt.plot(y_det, color='black', label='Deterministic')
    plt.legend()
    plt.title('ABM')
    plt.show()


brown_1 = abm(1, 10, 0.04, 0.4)
brown_2 = abm(1, 10, 0.04, 0.4)
brown_3 = abm(1, 10, 0.04, 0.4)
brown_deter = deterministic_brown(1, 10, 0.04)
draw(brown_1, brown_2, brown_3, brown_deter)
