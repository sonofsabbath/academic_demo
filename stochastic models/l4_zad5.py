import numpy as np
import matplotlib.pyplot as plt


def risk(lam_hpp, lam, t, mu, sig, cap, theta):
    """Generuje proces ryzyka oparty o NHPP z funkcją intenstywności lam, opraty o HPP o intensywności lam, w okresie t
        lat. Szkoda ma rozkład lognormalny o średniej mu i odchyleniu sig, kapitał początkowy wynosi cap, a względny
        narzut na bezpieczeństwo theta"""

    r = np.zeros(t * 365 + 1)
    r[0] = cap
    e = np.exp(mu + sig ** 2 / 2)
    due = (1 + theta) * e * lam_hpp

    n = np.random.poisson(lam_hpp * t)
    u = np.random.uniform(size=n)
    times = t * np.sort(u)

    ut = np.random.uniform(size=n)
    times_nhpp = []

    for i in range(len(ut)):
        t_year = i / 365
        if ut[i] < lam(t_year) / lam_hpp:
            times_nhpp.append(times[i])
    times_nhpp = np.array(times_nhpp)

    loss = np.random.lognormal(mu, sig, n)
    for i in range(1, t * 365 + 1):
        t_year = i / 365
        r[i] = cap + due * t_year - np.sum(loss[np.argwhere(times_nhpp <= t_year)])

    return r


def fan_chart(traj):
    """Generuje fan chart dla podanych trajektorii"""

    traj = traj.T
    perc = np.flip(np.arange(5, 50, 5))  # kwantyle do obliczenia (także 50 + perc)
    fig, ax = plt.subplots(figsize=(12, 5))
    colors = [(1, 240 / 255, 0), (1, 210 / 255, 0), (1, 180 / 255, 0), (1, 150 / 255, 0), (1, 120 / 255, 0),
              (1, 90 / 255, 0), (1, 60 / 255, 0), (1, 30 / 255, 0), (1, 0, 0)]  # paleta barw w RGBA

    for p in range(len(perc)):
        lower = np.percentile(traj, 50 - perc[p], axis=1)  # liczenie kwantyli
        higher = np.percentile(traj, 50 + perc[p], axis=1)
        x = np.linspace(0, T, len(lower))

        ax.fill_between(x, lower, higher, color=colors[p])  # "kolorowanie"
        ax.set_xlabel('t')
        ax.set_ylabel('R(t)')

    ax.set_title('NHPP risk')

    return fig, ax


def get_lambda(fun, t):
    """Szuka górnego ograniczenia podanej funkcji w zakresie od 0 do t"""

    x = np.arange(0, t, 0.1)
    vals = np.zeros(len(x))

    for i in range(len(vals)):
        vals[i] = fun(x[i])

    return np.max(vals)


T = 10
ruin = 0
risks = []
Lam = get_lambda(lambda x: 20 + 5 * np.sin(np.pi * T), T)

for i in range(1000):
    if (i + 1) % 100 == 0:
        print(f'Trajectory nr {i + 1}')

    rt = risk(Lam, lambda x: 20 + 5 * np.sin(np.pi * T), T, 18, 2, 100 * 10 ** 9, 0.4)
    risks.append(rt)

    if np.min(rt) < 0:
        ruin += 1

risks = np.array(risks)
risk_fig, risk_ax = fan_chart(risks)

risk_plots = np.random.randint(0, len(risks), 3)
colors = ['black', 'blue', 'green']
for i in range(len(risk_plots)):
    risk_ax.plot(np.linspace(0, T, len(risks[i])), risks[i], color=colors[i])

plt.show()
print(f'Ruin probability: {ruin / 1000}')
