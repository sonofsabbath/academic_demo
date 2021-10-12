import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def explore_daily(data, col_label, day):
    """Zwraca szukane wartości dla dobowego poziomu sezonowości w danym dniu tygodnia"""

    select_data = data.loc[data['Weekday'] == day]
    hour_vals = []

    for i in range(24):
        hour_data = select_data.loc[select_data['Hour'] == i]
        hour_vals.append(list(hour_data[col_label]))

    return np.array(hour_vals).T


def explore_weekly(data, col_label):
    """Zwraca szukane wartości dla tygodniowego poziomu sezonowości"""

    week_vals = []

    for day in range(1, 8):
        weekday_vals = []
        select_data = data.loc[data['Weekday'] == day]
        dates = select_data['Date'].unique()

        for date in dates:
            daily_vals = select_data.loc[select_data['Date'] == date]
            weekday_vals.append(daily_vals[col_label].mean())

        if len(weekday_vals) == 163:
            weekday_vals = weekday_vals[:-1]
        week_vals.append(weekday_vals)

    return np.array(week_vals).T


def get_pdh_zdh(data):
    """Wyciąga wartości Pdh i Zdh"""

    pdh = np.array(data['System price'])
    zdh = np.array(data['Consumption forecast'])

    return pdh, zdh


def get_pdh_pdkh(data, k, h):
    """Wyciąga wartości Pdh i P(d-k)h dla danego k oraz dla godzin h[0]:h[1]:h[2]"""

    hours = np.arange(h[0]-1, h[2], h[1])
    select_data = data.loc[data['Hour'].isin(hours)]

    pdh = np.array(select_data['System price'])[:len(select_data) - k*len(hours)]
    pdkh = np.array(select_data['System price'])[k*len(hours):]

    return pdh, pdkh


def draw_seasonal(data, title, val_label, mode, weekly=False):
    """Rysuje wykresy sezonowe dla podanych danych i poziomu sezonowości"""

    plt.figure(figsize=(10, 4.8))

    if mode == 1:
        for i in data:
            plt.plot(i)
    else:
        data = data.T
        for i in range(len(data)):
            points = np.linspace(i - 0.4, i + 0.4, len(data[i]))
            plt.plot(points, data[i])
            plt.plot(points, np.ones(len(data[i])) * np.mean(data[i]), color='black')

    if not weekly:
        plt.xticks(np.arange(0, 24))
        plt.xlabel('Hour')
    else:
        plt.xticks(np.arange(0, 7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        plt.xlabel('Weekday')

    plt.title(title)
    plt.ylabel(val_label)
    plt.show()


def draw(data_x, data_y, title, labels):
    """Rysuje wykresy punktowe Pdh vs Zdh (lub Pdh vs P(d-k)h)"""

    plt.scatter(data_x, data_y)
    plt.title(title)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.show()


nordpool = pd.read_csv('NPdata_2013-2016.txt', header=None, delimiter='   ', engine='python')
nordpool.columns = ['Date', 'Hour', 'System price', 'Consumption forecast', 'del']
nordpool.drop(labels='del', axis=1, inplace=True)
nordpool['Date'] = nordpool['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
nordpool['Weekday'] = nordpool['Date'].dt.weekday + 1

tuesday_zp = explore_daily(nordpool, 'System price', 2)
sunday_zp = explore_daily(nordpool, 'System price', 7)
tuesday_sl = explore_daily(nordpool, 'Consumption forecast', 2)
sunday_sl = explore_daily(nordpool, 'Consumption forecast', 7)

draw_seasonal(tuesday_zp, 'Seasonal plot - Tuesdays', 'System price', 1)
draw_seasonal(sunday_zp, 'Seasonal plot - Sundays', 'System price', 1)
draw_seasonal(tuesday_sl, 'Seasonal plot - Tuesdays', 'Consumption forecast', 1)
draw_seasonal(sunday_sl, 'Seasonal plot - Sundays', 'Consumption forecast', 1)

draw_seasonal(tuesday_zp, 'Seasonal plot - Tuesdays', 'System price', 2)
draw_seasonal(sunday_zp, 'Seasonal plot - Sundays', 'System price', 2)
draw_seasonal(tuesday_sl, 'Seasonal plot - Tuesdays', 'Consumption forecast', 2)
draw_seasonal(sunday_sl, 'Seasonal plot - Sundays', 'Consumption forecast', 2)

weekly_zp = explore_weekly(nordpool, 'System price')
weekly_sl = explore_weekly(nordpool, 'Consumption forecast')

draw_seasonal(weekly_zp, 'Seasonal plot - weekdays', 'System price', 1, True)
draw_seasonal(weekly_sl, 'Seasonal plot - weekdays', 'Consumption forecast', 1, True)

draw_seasonal(weekly_zp, 'Seasonal plot - weekdays', 'System price', 2, True)
draw_seasonal(weekly_sl, 'Seasonal plot - weekdays', 'Consumption forecast', 2, True)

p, z = get_pdh_zdh(nordpool)
draw(p, z, '$P_{dh}$ vs $Z_{dh}$', ['$P_{dh}$', '$Z_{dh}$'])

for i in range(9):
    pd, pdk = get_pdh_pdkh(nordpool, i + 1, [4, 4, 24])
    draw(pd, pdk, '$P_{dh}$ vs $P_{(d-k)h}$, k=' + str(i + 1), ['$P_{dh}$', '$P_{(d-k)h}$'])
