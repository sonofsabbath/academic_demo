import numpy as np
import matplotlib.pyplot as plt

N = 1000
I0 = 1
Beta = 0.5
Sigma = 0.1
Gamma = 0.1
Eta = 0.2
Dt = 1 / 144


def stochastic_seir(n, i0, beta, gamma, sigma, dt, t):
    """Generuje trajektorię stochastycznego  modelu SEIR dla populacji o liczebności n, początkowej liczby zarażonych
        i0, stopy infekcji beta, stopy wyzdrowień gamma, stopy sigma i kroku dt w czasie t"""

    x = np.arange(0, t + dt, dt)
    s = np.zeros(len(x))
    e = np.zeros(len(x))
    i = np.zeros(len(x))
    r = np.zeros(len(x))
    s[0] = n - i0
    e[0] = 0
    i[0] = i0
    r[0] = 0
    u1 = np.random.uniform(size=len(x) - 1)  # losowe wartości z rozkładu U(0, 1)
    u2 = np.random.uniform(size=len(x) - 1)
    u3 = np.random.uniform(size=len(x) - 1)

    for it in range(1, len(x)):
        p1 = beta * (i[it - 1] * s[it - 1] / N ** 2)  # prawdopodobieństwo przejścia ze stanu S do stanu E
        p2 = sigma * (e[it - 1] / N)  # prawdopodobieństwo E -> I
        p3 = gamma * (i[it - 1] / N)  # prawdopodobieństwo I -> R

        if u1[it - 1] < p1:
            s[it] = s[it - 1] - 1
            e[it] = e[it - 1] + 1
        else:
            s[it] = s[it - 1]
            e[it] = e[it - 1]

        if u2[it - 1] < p2:
            e[it] = e[it - 1] - 1
            i[it] = i[it - 1] + 1
        else:
            i[it] = i[it - 1]

        if u3[it - 1] < p3:
            i[it] = i[it - 1] - 1
            r[it] = r[it - 1] + 1
        else:
            r[it] = r[it - 1]

    return s, e, i, r


def stochastic_seirs(n, i0, beta, gamma, eta, sigma, dt, t):
    """Generuje trajektorię stochastycznego modelu SEIR dla populacji o liczebności n, początkowej liczby zarażonych i0,
        stopy infekcji beta, stopy wyzdrowień gamma, stopy sigma, stopy eta i kroku dt w czasie t"""

    x = np.arange(0, t + dt, dt)
    s = np.zeros(len(x))
    e = np.zeros(len(x))
    i = np.zeros(len(x))
    r = np.zeros(len(x))
    s[0] = n - i0
    e[0] = 0
    i[0] = i0
    r[0] = 0
    u1 = np.random.uniform(size=len(x) - 1)  # losowe wartości z rozkładu U(0, 1)
    u2 = np.random.uniform(size=len(x) - 1)
    u3 = np.random.uniform(size=len(x) - 1)
    u4 = np.random.uniform(size=len(x) - 1)

    for it in range(1, len(x)):
        p1 = beta * (i[it - 1] * s[it - 1] / N ** 2)  # prawdopodobieństwo przejścia ze stanu S do stanu E
        p2 = sigma * (e[it - 1] / N)  # prawdopodobieństwo E -> I
        p3 = gamma * (i[it - 1] / N)  # prawdopodobieństwo I -> R
        p4 = eta * (r[it - 1] / N)  # prawdopodobieństwo R -> S

        if u1[it - 1] < p1:
            s[it] = s[it - 1] - 1
            e[it] = e[it - 1] + 1
        else:
            s[it] = s[it - 1]
            e[it] = e[it - 1]

        if u2[it - 1] < p2:
            e[it] = e[it - 1] - 1
            i[it] = i[it - 1] + 1
        else:
            i[it] = i[it - 1]

        if u3[it - 1] < p3:
            i[it] = i[it - 1] - 1
            r[it] = r[it - 1] + 1
        else:
            r[it] = r[it - 1]

        if u4[it - 1] < p4:
            r[it] = r[it - 1] - 1
            s[it] = s[it - 1] + 1

    return s, e, i, r


def generate_trajectories(model, n, dt, t):
    """Generuje n trajektorii wybranego modelu"""

    x = np.arange(0, t + dt, dt)
    s_traj = np.zeros((n, len(x)))
    e_traj = np.zeros((n, len(x)))
    i_traj = np.zeros((n, len(x)))
    r_traj = np.zeros((n, len(x)))

    for i in range(n):  # wyznaczanie trajektorii
        print('{}: generating trajectory {} of {}'.format(model, i + 1, n))
        if model == 'SEIR':
            mod_s, mod_e, mod_i, mod_r = stochastic_seir(N, I0, Beta, Gamma, Sigma, dt, t)
        else:
            mod_s, mod_e, mod_i, mod_r = stochastic_seirs(N, I0, Beta, Gamma, Eta, Sigma, dt, t)
        s_traj[i] = mod_s
        e_traj[i] = mod_e
        i_traj[i] = mod_i
        r_traj[i] = mod_r

    s_traj = s_traj.T  # transpozycja
    e_traj = e_traj.T
    i_traj = i_traj.T
    r_traj = r_traj.T

    return x, s_traj, e_traj, i_traj, r_traj


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


seir_x, seir_s, seir_e, seir_i, seir_r = generate_trajectories('SEIR', 100, Dt, 1000)
seir_s_fig, seir_s_ax = fan_chart('Stochastic SEIR: state S', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\sigma$'],
                                  [N, I0, Beta, Gamma, Sigma], seir_x, seir_s)
plt.show()
seir_e_fig, seir_e_ax = fan_chart('Stochastic SEIR: state E', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\sigma$'],
                                  [N, I0, Beta, Gamma, Sigma], seir_x, seir_e)
plt.show()
seir_i_fig, seir_i_ax = fan_chart('Stochastic SEIR: state I', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\sigma$'],
                                  [N, I0, Beta, Gamma, Sigma], seir_x, seir_i)
plt.show()
seir_r_fig, seir_r_ax = fan_chart('Stochastic SEIR: state R', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\sigma$'],
                                  [N, I0, Beta, Gamma, Sigma], seir_x, seir_r)
plt.show()

seirs_x, seirs_s, seirs_e, seirs_i, seirs_r = generate_trajectories('SEIRS', 100, Dt, 700)
seirs_s_fig, seirs_s_ax = fan_chart('Stochastic SEIRS: state S', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\sigma$'],
                                  [N, I0, Beta, Gamma, Sigma], seirs_x, seirs_s)
plt.show()
seirs_e_fig, seirs_e_ax = fan_chart('Stochastic SEIRS: state E', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\sigma$'],
                                  [N, I0, Beta, Gamma, Sigma], seirs_x, seirs_e)
plt.show()
seirs_i_fig, seirs_i_ax = fan_chart('Stochastic SEIRS: state I', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\sigma$'],
                                  [N, I0, Beta, Gamma, Sigma], seirs_x, seirs_i)
plt.show()
seirs_r_fig, seirs_r_ax = fan_chart('Stochastic SEIRS: state R', ['[N', r'$I_0$', r'$\beta$', r'$\gamma$', r'$\sigma$'],
                                  [N, I0, Beta, Gamma, Sigma], seirs_x, seirs_r)
plt.show()
