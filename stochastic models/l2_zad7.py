import numpy as np
import matplotlib.pyplot as plt

N = 1000
I0 = 1
Beta = 0.5
Gamma = 0.1
Eta = 0.2
Dt = 1 / 96


def stochastic_si(n, i0, beta, dt, t):
    """Generuje trajektorię stochastycznego modelu SI dla populacji o liczebności n, początkowej liczby
        zarażonych i0, stopy infekcji beta i kroku dt w czasie t"""

    x = np.arange(0, t + dt, dt)  # wektor wartości z zakresu [0, t+dt) o różnicach równych dt (punkty w czasie)
    s = np.zeros(len(x))  # inicjalizacja wektorów S oraz I
    i = np.zeros(len(x))
    s[0] = n - i0  # warunki początkowe
    i[0] = i0
    u = np.random.uniform(size=len(x)-1)  # losowe wartości z rozkładu U(0, 1)

    for it in range(1, len(x)):
        p = beta * ((i[it - 1] * s[it - 1]) / N ** 2)  # prawdopodobieństwo przejścia ze stanu S do stanu I

        if u[it - 1] < p:  # decyzja o zmianie lub jej braku
            s[it] = s[it - 1] - 1
            i[it] = i[it - 1] + 1
        else:
            s[it] = s[it - 1]
            i[it] = i[it - 1]

    return s, i


def stochastic_sis(n, i0, beta, gamma, dt, t):
    """Generuje trajektorię stochastycznego modelu SIS dla populacji o liczebności n, początkowej liczby zarażonych i0,
        stopy infekcji beta, stopy wyzdrowień gamma i kroku dt w czasie t"""

    x = np.arange(0, t + dt, dt)
    s = np.zeros(len(x))
    i = np.zeros(len(x))
    s[0] = n - i0
    i[0] = i0
    u1 = np.random.uniform(size=len(x) - 1)  # losowe wartości z rozkładu U(0, 1)
    u2 = np.random.uniform(size=len(x) - 1)

    for it in range(1, len(x)):
        p1 = beta * (i[it - 1] * s[it - 1] / N ** 2)  # prawdopodobieństwo przejścia ze stanu S do stanu I
        p2 = gamma * (i[it - 1] / N)  # prawdopodobieństwo I -> S

        if u1[it - 1] < p1:
            s[it] = s[it - 1] - 1
            i[it] = i[it - 1] + 1
        else:
            s[it] = s[it - 1]
            i[it] = i[it - 1]

        if u2[it - 1] < p2:
            s[it] = s[it - 1] + 1
            i[it] = i[it - 1] - 1

    return s, i


def stochastic_sirs(n, i0, beta, gamma, eta, dt, t):
    """Generuje trajektorię stochastycznego modelu SIRS dla populacji o liczebności n, początkowej liczby zarażonych i0,
        stopy infekcji beta, stopy wyzdrowień gamma, stopy eta i kroku dt w czasie t"""

    x = np.arange(0, t + dt, dt)
    s = np.zeros(len(x))
    i = np.zeros(len(x))
    r = np.zeros(len(x))
    s[0] = n - i0
    i[0] = i0
    r[0] = 0
    u1 = np.random.uniform(size=len(x) - 1)  # losowe wartości z rozkładu U(0, 1)
    u2 = np.random.uniform(size=len(x) - 1)
    u3 = np.random.uniform(size=len(x) - 1)

    for it in range(1, len(x)):
        p1 = beta * (i[it - 1] * s[it - 1] / N ** 2)  # prawdopodobieństwo przejścia ze stanu S do stanu I
        p2 = gamma * (i[it - 1] / N)  # prawdopodobieństwo I -> R
        p3 = eta * (r[it - 1] / N)  # prawdopodobieństwo R -> S

        if u1[it - 1] < p1:
            s[it] = s[it - 1] - 1
            i[it] = i[it - 1] + 1
        else:
            s[it] = s[it - 1]
            i[it] = i[it - 1]

        if u2[it - 1] < p2:
            i[it] = i[it - 1] - 1
            r[it] = r[it - 1] + 1
        else:
            r[it] = r[it - 1]  # S oraz I zostały już wyznaczone wyżej

        if u3[it - 1] < p3:
            r[it] = r[it - 1] - 1
            s[it] = s[it - 1] + 1

    return s, i, r


def generate_trajectories(model, n, dt, t):
    """Generuje n trajektorii wybranego modelu"""

    x = np.arange(0, t + dt, dt)
    s_traj = np.zeros((n, len(x)))
    i_traj = np.zeros((n, len(x)))
    if model == 'SIRS':
        r_traj = np.zeros((n, len(x)))

    for i in range(n):  # wyznaczanie trajektorii
        print('{}: generating trajectory {} of {}'.format(model, i + 1, n))
        if model == 'SI':
            mod_s, mod_i = stochastic_si(N, I0, Beta, Dt, t)
        elif model == 'SIS':
            mod_s, mod_i = stochastic_sis(N, I0, Beta, Gamma, Dt, t)
        else:
            mod_s, mod_i, mod_r = stochastic_sirs(N, I0, Beta, Gamma, Eta, Dt, t)
            r_traj[i] = mod_r
        s_traj[i] = mod_s
        i_traj[i] = mod_i

    s_traj = s_traj.T  # transpozycja
    i_traj = i_traj.T
    if model == 'SIRS':
        r_traj = r_traj.T
        return x, s_traj, i_traj, r_traj
    return x, s_traj, i_traj


def fan_chart(model_title, model_params, param_vals, x, traj):
    """Generuje wykresy typu fan chart dla podanych trajektorii"""

    perc = np.flip(np.arange(5, 50, 5))  # kwantyle do obliczenia (także 50 + perc)
    fig, ax = plt.subplots()
    colors = [(1, 240 / 255, 0), (1, 210 / 255, 0), (1, 180 / 255, 0), (1, 150 / 255, 0), (1, 120 / 255, 0),
              (1, 90 / 255, 0), (1, 60 / 255, 0), (1, 30 / 255, 0), (1, 0, 0)]  # paleta barw w RGBA

    for p in range(len(perc)):
        print('{} - calculating percentiles {} and {}'.format(model_title, 50 - perc[p], 50 + perc[p]))
        lower = np.percentile(traj, 50 - perc[p], axis=1)  # liczenie kwantyli
        higher = np.percentile(traj, 50 + perc[p], axis=1)
        ax.fill_between(x, lower, higher, color=colors[p])  # "kolorowanie"
        ax.set_xlabel('Time')
        ax.set_ylabel('Number of people')

    for i in range(len(model_params)):
        model_title += " {}={},".format(model_params[i], param_vals[i])
    model_title = model_title[:-1] + ']'
    ax.set_title(model_title)
    ax.set_ylim(0, 1010)

    return fig, ax


si_x, si_s, si_i = generate_trajectories('SI', 100, Dt, 250)
si_s_fig, si_s_ax = fan_chart('Stochastic SI: state S', ['[N', r'$I_0$', r'$\beta$'], [N, I0, Beta], si_x, si_s)
plt.show()
si_i_fig, si_i_ax = fan_chart('Stochastic SI: state I', ['[N', r'$I_0$', r'$\beta$'], [N, I0, Beta], si_x, si_i)
plt.show()

sis_x, sis_s, sis_i = generate_trajectories('SIS', 100, Dt, 500)
sis_s_fig, sis_s_ax = fan_chart('Stochastic SIS: state S', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$'],
                                [N, I0, Beta, Gamma], sis_x, sis_s)
plt.show()
sis_i_fig, sis_i_ax = fan_chart('Stochastic SIS: state I', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$'],
                                [N, I0, Beta, Gamma], sis_x, sis_i)
plt.show()

sirs_x, sirs_s, sirs_i, sirs_r = generate_trajectories('SIRS', 100, Dt, 400)
sirs_s_fig, sirs_s_ax = fan_chart('Stochastic SIRS: state S', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\eta$'],
                                  [N, I0, Beta, Gamma, Eta], sirs_x, sirs_s)
plt.show()
sirs_i_fig, sirs_i_ax = fan_chart('Stochastic SIRS: state I', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\eta$'],
                                  [N, I0, Beta, Gamma, Eta], sirs_x, sirs_i)
plt.show()
sirs_r_fig, sirs_r_ax = fan_chart('Stochastic SIRS: state R', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\eta$'],
                                  [N, I0, Beta, Gamma, Eta], sirs_x, sirs_r)
plt.show()
