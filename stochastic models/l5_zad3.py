import numpy as np
import matplotlib.pyplot as plt


def rule_output(bits):
    """Przyjmuje wartości komórek i jej sąsiadów, zwraca nowy stan komórki"""

    left, center, right = bits
    output = 7 - (4 * left + 2 * center + right)

    return output


def wolfram(init_state, rule_decimal, n):
    """Wyznacza n stanów automatu Wolframa dla zasady rule_decimal, zaczynając od stanu init_state"""

    rule = np.binary_repr(rule_decimal, 8)
    rule = np.array([int(i) for i in rule])

    automaton = np.zeros((n, len(init_state)), dtype=np.int8)
    automaton[0, :] = init_state

    for i in range(1, n):
        prev_state = automaton[i - 1, :]
        bit_groups = np.stack([np.roll(prev_state, 1), prev_state, np.roll(prev_state, -1)])

        automaton[i, :] = rule[np.apply_along_axis(rule_output, 0, bit_groups)]

    return automaton


def draw_cells(rule, state_len, n_states, initial=None, single=False):
    """Wyświetla wizualizację automatu dla reguły rule, domyślnie dla inicjalizacji losowej"""

    if initial is None:
        if single:
            initial = np.zeros(state_len, dtype=np.int8)
            initial[int(np.round(state_len / 2))] = 1
            title_add = 'Single cell initialization'
        else:
            initial = np.random.randint(0, 2, 300)
            title_add = 'Random initialization'
    else:
        title_add = 'Custom initialization'

    cells = wolfram(initial, rule, n_states)

    plt.rcParams['image.cmap'] = 'binary'
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.set_title(f'Cellular automaton - rule {rule} ({title_add})')
    ax.set_xlabel('Bits')
    ax.set_ylabel('State')
    ax.matshow(cells)
    plt.show()


draw_cells(105, 300, 100)
draw_cells(105, 300, 100)
draw_cells(105, 300, 100, single=True)

init_custom1 = np.zeros(300)
init_custom2 = np.zeros(300)

for i in range(len(init_custom1)):
    if i % 2 == 0:
        init_custom1[i] = 1
    if i % 10 == 0:
        init_custom2[i] = 1

draw_cells(105, 300, 100, init_custom1)
draw_cells(105, 300, 100, init_custom2)
