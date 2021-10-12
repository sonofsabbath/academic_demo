import numpy as np

# matrix = np.array([[1, 5, 3, 2],
#                    [1/5, 1, 3, 1],
#                    [1/3, 1/3, 1, 1/5],
#                    [1/2, 1, 5, 1]])


def global_wages(matrix):
    k = matrix
    k = k.tolist()
    k.append([])

    # sumowanie wartości ocen w kolumnach
    for i in range(matrix.shape[0]):
        k[-1].append(sum(matrix[:, i]))
    k = np.array(k)

    # dzielenie wartości w kolumnach przez wyliczone sumy
    for i in range(k.shape[0]):
        for j in range(k.shape[1]):
            k[i][j] = k[i][j]/k[-1][j]
    k = k.tolist()
    list = []

    # średnia arytmetyczna wierszy - wagi kryteriów
    for i in range(matrix.shape[0]):
        k[i].append(sum(k[i][:])/matrix.shape[0])
        list.append(k[i][-1])
    return list


#wagi = global_wages(matrix)
# print(wagi)
# print(sum(wagi))
