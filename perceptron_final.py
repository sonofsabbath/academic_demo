import numpy as np
import matplotlib.pyplot as plt


def wpr_dane():
    data = []
    f = input('u - funkcja unipolarna\nb - funkcja bipolarna\n')

    for i in range(4):
        print('Rekord ' + str(i+1) + '.:')
        x1 = int(input())
        x2 = int(input())
        y = int(input())
        data.append([x1, x2, y])
    return data, f


def f_aktywacji(rekord, waga):
    s = waga[0]
    for i in range(len(rekord) - 1):
        s += waga[i+1] * rekord[i]

    if s > 0:
        return 1
    elif funkcja == 'u':
        return 0
    else:
        return -1


def korekta_wag(dane, wsp_uczenia, epoki):
    wagi = np.random.rand(3)
    for i in range(epoki):
        suma_bledow = 0
        for j in dane:
            wynik = f_aktywacji(j, wagi)
            blad = j[-1] - wynik
            suma_bledow += np.abs(blad)

            wagi[0] += wsp_uczenia * blad
            for k in range(len(j) - 1):
                wagi[k+1] += wsp_uczenia * blad * j[k]

        print('Epoka: ' + str(i+1) + '   Suma błędów: ' + str(suma_bledow))
        x1 = np.linspace(-1, 2)
        x2 = -((wagi[0] + wagi[1] * x1) / wagi[2])
        plt.plot(x1, x2)
        if funkcja == 'u':
            plt.scatter([1, 1, 0, 0], [1, 0, 1, 0])
        else:
            plt.scatter([1, 1, -1, -1], [1, -1, 1, -1])
        plt.show()

        if suma_bledow == 0:
            break
    return wagi


def test(wag):
    x = int(input('1 - przeprowadź test\n0 - zakończ\n'))
    if x == 0:
        return 0
    else:
        print('Wprowadź dane wejściowe:')
        x1 = int(input())
        x2 = int(input())
        print(f_aktywacji([x1, x2, 0], wag))
        test(wag)


dataset, funkcja = wpr_dane()
wagi = korekta_wag(dataset, 0.1, 20)
print(wagi)
test(wagi)
