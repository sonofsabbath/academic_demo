import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression


def estimate_R0(confirmed, deaths, recovered, country, from_date, to_date, serial):
    """Estymuje wartości 7-dniowego współczynnika R0 dla ewolucji epidemii COVID-19 w danym kraju, na danym przedziale
        czasowym oraz dla danej wartości Tr"""

    # wyciągnięcie danych dla konkretnego kraju
    confirmed_in_country = confirmed.loc[confirmed['Country/Region'] == country].copy()
    deaths_in_country = deaths.loc[deaths['Country/Region'] == country].copy()
    recovered_in_country = recovered.loc[recovered['Country/Region'] == country].copy()
    dates = pd.date_range(from_date, to_date)  # lista dni

    change_date = {}  # przerzucenie nazw kolumn na format datetime64
    for i in list(confirmed_in_country.columns[4:]):
        change_date[i] = pd.to_datetime(i)  # tworzenie słownika {stara_nazwa: nowa_nazwa}
    confirmed_in_country.rename(columns=change_date, inplace=True)  # zmiana nazw
    deaths_in_country.rename(columns=change_date, inplace=True)
    recovered_in_country.rename(columns=change_date, inplace=True)

    infected = np.zeros(len(dates))
    for d in range(len(dates)):  # obliczanie log(It)
        infected[d] = np.log(confirmed_in_country[dates[d]].values - deaths_in_country[dates[d]].values
                             - recovered_in_country[dates[d]].values)

    gamma = 1 / serial
    days = len(dates) - 6
    r0 = np.zeros(days)

    for i in range(days):  # regresja liniowa na podstawie 7-dniowych okresów
        x = np.arange(7).reshape((-1, 1))  # przygotowanie danych
        y = infected[i:i+7]

        model = LinearRegression()  # inicjacja modelu regresji liniowej
        model.fit(x, y)  # dopasowanie prostej
        alpha = model.coef_  # wyciągnięcie nachylenia prostej

        r0[i] = alpha / gamma + 1

    return dates, r0


def draw(days, r0, country, tr):
    """Rysuje wykres wyestymowanych wartości R0 dla danego kraju w danych dniach"""

    ticks = np.arange(0, len(r0), 10)
    labels = []
    for i in range(len(ticks)):
        labels.append(str(days[10 * i])[:-9])

    plt.figure(figsize=(8, 4.8))
    plt.plot(r0, label="$R_0$ (7 days mean)")
    plt.plot(range(len(R0)), np.ones(len(R0)), '--', label="$R_0$ = 1")
    plt.xticks(ticks, labels, rotation='vertical')
    plt.ylim(0, max(R0) + 0.1)
    plt.legend()
    plt.title("Estimated $R_0$ for {}, $T_r$ = {}".format(country, tr))
    plt.show()


confirmed_data = pd.read_csv('confirmed.csv')
deaths_data = pd.read_csv('deaths.csv')
recovered_data = pd.read_csv('recovered.csv')
Tr = 5.2
countries = ['Argentina', 'Germany', 'Japan']

for c in countries:
    Days, R0 = estimate_R0(confirmed_data, deaths_data, recovered_data, c, '3/4/20', '3/22/21', Tr)
    draw(Days[6:], R0, c, Tr)
