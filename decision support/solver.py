import pulp
import numpy as np
import pandas as pd

# brakuje w bazie ładunku użytecznego i systemów, trzeba będzie dopisać po uzupełnieniu
def eliminate(perfect, max_t):
    """Wstępne przefiltrowanie samolotów, żeby odciążyć solver, odpowiednik ograniczeń: 1, 3, 4, 5
    (tak, wiem, niezbyt profesjonalnie, ale inaczej się ze mną kłóci :()
    perfect - wektor z parametrami samolotu "idealnego" [V, R, C, E, H]
    max_t - deadline na skompletowanie floty"""
    p = 0
    for i in planes:
        if run_up[i] > perfect[3] or height[i] < perfect[4] or time[i] > max_t:
            del(planes[p])
            del(velocity[i])
            del(ranges[i])
            del(cost[i])
            del(run_up[i])
            del(height[i])
            del(time[i])
        p += 1


def choose_planes(plane_items, perfect, u, v, r, t, p, max_p, M):
    """"Solver
    plane_items - lista z nazwami samolotów
    perfect - wektor z parametrami samolotu idealnego [V, R, C, E, H]
    u - wektor wag [uv, ur, uc, ut, ua]
    v, r, c, t, p - słowniki z parametrami samolotów w formacie {model: wartość}
    max_p - budżet
    M - ilość samolotów do kupienia"""
    # definicja problemu i zmiennych
    problem = pulp.LpProblem("Army_planes_problem", pulp.LpMinimize)
    s = pulp.LpVariable.dicts("Planes", plane_items, lowBound=0, cat='Integer')
    x = pulp.LpVariable.dicts("Models", plane_items, 0, 1, cat='Integer')

    # funkcja celu (brakuje systemów i ładunku)
    problem += pulp.lpSum([s[i] * (u[0] * (perfect[0] - v[i]) + u[1] * (perfect[1] - r[i]))]
                          for i in plane_items) + np.max([x[p] * t[p]] for p in plane_items)

    # ograniczenia (brakuje 7, 8)
    problem += pulp.lpSum([s[i] * p[i]] for i in plane_items) <= max_p  # 2
    problem += pulp.lpSum([s[i]] for i in plane_items) == M  # 6
    for i in plane_items:
        problem += x[i] >= 10 ** -8 * s[i]  # 9

    # rozwiązanie
    problem.solve()
    lista = []
    for v in problem.variables():
        if v.varValue > 0:
            print(v.name, "=", v.varValue)
            lista.append(f'{v.name} = {v.varValue}')
    return lista


# przygotowanie danych
df = pd.read_excel('airbaza.xlsx')
planes = list(df['Nazwa'])
velocity = dict(zip(planes, df['Predkosc']))
ranges = dict(zip(planes, df['Zasieg']))
cost = dict(zip(planes, df['Koszt']))
run_up = dict(zip(planes, df['Rozbieg']))
height = dict(zip(planes, df['Pulap']))
time = dict(zip(planes, df['Realizacja']))

# print("Wstępne filtrowanie")
# eliminate([1800, 3000, 10000, 400, 15], 6)
# print("Szukanie optymalnego rozwiązania")
# choose_planes(planes, [1800, 3000, 10000, 400, 15], [0.5, 0.3, 0.2,0.5, 0.3, 0.2,0.5, 0.3, 0.2], velocity, ranges, time, cost, 5000, 10)
