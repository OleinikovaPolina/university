import copy
import random


def liner_fitting(data_x, data_y):
    size = len(data_x)
    i = 0
    sum_xy = 0
    sum_y = 0
    sum_x = 0
    sum_sqare_x = 0
    size2 = 0
    while i < size:
        if data_x[i] is not None and data_y[i] is not None:
            sum_xy += data_x[i] * data_y[i]
            sum_y += data_y[i]
            sum_x += data_x[i]
            sum_sqare_x += data_x[i] * data_x[i]
            size2 += 1
        i += 1
    if size2 == 0:
        return [None, None]
    average_x = sum_x / size2
    average_y = sum_y / size2
    if size2 * sum_sqare_x - sum_x * sum_x == 0:
        return [None, None]
    return_k = (size2 * sum_xy - sum_x * sum_y) / (size2 * sum_sqare_x - sum_x * sum_x)
    return_b = average_y - average_x * return_k
    return [return_k, return_b]


def calculate(data_x, data_y, k, b):
    size = len(data_x)
    i = 0
    while i < size:
        if data_x[i] is None and data_y[i] is not None:
            data_x[i] = int((data_y[i] - b) / k)
        if data_y[i] is None and data_x[i] is not None:
            data_y[i] = int(k * data_x[i] + b)
        i += 1
    return data_x, data_y


def corrcoef(x, y):
    x_avg = sum(x) / len(x)
    y_avg = sum(y) / len(y)
    x_var = sum((i - x_avg) ** 2 for i in x)
    y_var = sum((i - y_avg) ** 2 for i in y)
    newvar = (x_var * y_var) ** 0.5
    newvar2 = sum((x[i] - x_avg) * (y[i] - y_avg) for i in range(len(x)))
    return newvar, newvar2


def for_corrcoef(matrix):
    # rows
    matrixCoef = [[1] * len(matrix) for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(i, len(matrix)):
            x = []
            y = []
            for z in range(len(matrix)):
                if matrix[i][z] is not None and matrix[j][z] is not None:
                    x.append(matrix[i][z])
                    y.append(matrix[j][z])
            if len(x) == 0:
                matrixCoef[i][j] = None
                matrixCoef[j][i] = None
                break
            newvar, newvar2 = corrcoef(x, y)
            if newvar == 0:
                matrixCoef[i][j] = None
                matrixCoef[j][i] = None
                break
            matrixCoef[i][j] = round(newvar2 / newvar, 4)
            matrixCoef[j][i] = round(newvar2 / newvar, 4)
    print('\nКоэффициенты корреляции Пиросна (Если убрать Nones)')
    print('    ', ' '.join(['{:6d}r'.format(i) for i in range(len(matrixCoef))]))
    for i in range(len(matrixCoef)):
        print('{:3d}r'.format(i), ' '.join(
            map(lambda x: 'None' if x is None else '{}{:.4f}'.format('' if x < 0 else '+', x), matrixCoef[i])))
    # columns
    matrixCoef = [[1] * len(matrix) for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(i, len(matrix)):
            x = []
            y = []
            for z in range(len(matrix)):
                if matrix[z][i] is not None and matrix[z][j] is not None:
                    x.append(matrix[z][i])
                    y.append(matrix[z][j])
            if len(x) == 0:
                matrixCoef[i][j] = None
                matrixCoef[j][i] = None
                break
            newvar, newvar2 = corrcoef(x, y)
            if newvar == 0:
                matrixCoef[i][j] = None
                matrixCoef[j][i] = None
                break
            matrixCoef[i][j] = round(newvar2 / newvar, 4)
            matrixCoef[j][i] = round(newvar2 / newvar, 4)
    print('\nКоэффициенты корреляции Пиросна (Если убрать Nones)')
    print('    ', ' '.join(['{:6d}c'.format(i) for i in range(len(matrixCoef))]))
    for i in range(len(matrixCoef)):
        print('{:3d}c'.format(i), ' '.join(
            map(lambda x: 'None' if x is None else '{}{:.4f}'.format('' if x < 0 else '+', x), matrixCoef[i])))


def print_table(matrix):
    print('    ', ' '.join(['{:3d}c'.format(i) for i in range(len(matrix))]))
    for i in range(len(matrix)):
        print('{:3d}r'.format(i), ' '.join(map(lambda x: 'None' if x is None else '{:4d}'.format(x), matrix[i])))


def create_tale():
    # read n
    n = int(input('Введите n>3\n'))
    if n < 4:
        return create_tale()
    # generate
    matrix = [[random.randint(1, 30) for j in range(n)] for i in range(n)]
    matrix0 = copy.deepcopy(matrix)
    # delete 10
    i = 0
    while i < 10:
        a1, a2 = random.randint(0, n - 1), random.randint(0, n - 1)
        if matrix[a1][a2] is not None:
            matrix[a1][a2] = None
            i += 1

    return matrix0, matrix


def get_rows(matrix):
    n1, n2 = map(str, input('\nВведите ряды\n').split())
    # rows
    if n1.find('r') > 0 and n2.find('r') > 0:
        n1 = n1.replace('r', '')
        n2 = n2.replace('r', '')
        if n1.isdigit() and n2.isdigit():
            if n1 == n2:
                print('ряды должны быть разные')
                return get_rows(matrix)
            return [0, n1, n2, matrix[int(n1)], matrix[int(n2)]]
    # columns
    elif n1.find('c') > 0 and n2.find('c') > 0:
        n1 = n1.replace('c', '')
        n2 = n2.replace('c', '')
        if n1.isdigit() and n2.isdigit():
            if n1 == n2:
                print('ряды должны быть разные')
                return get_rows(matrix)
            n1 = int(n1)
            n2 = int(n2)
            return 1, n1, n2, [e[n1] for e in matrix], [e[n2] for e in matrix]

    return get_rows(matrix)


def set_rows(type, n1, n2, x, y, matrix):
    # rows
    if type == 0:
        matrix[int(n1)], matrix[int(n2)] = x, y
    # columns
    if type == 1:
        for i in range(len(matrix)):
            matrix[i][n1] = x[i]
            matrix[i][n2] = y[i]
    return matrix


def corr(matrix):
    for_corrcoef(matrix)
    typeRow, n_1, n_2, x, y = get_rows(matrix)
    parameter = liner_fitting(x, y)
    if parameter[0] == None:
        print('ряды нельзя восстановить друг через друга')
        corr(matrix)
        return matrix
    x, y, = calculate(x, y, parameter[0], parameter[1])
    matrix = set_rows(typeRow, n_1, n_2, x, y, matrix)
    print_table(matrix)
    cont = input('\nВведите 1, если хотите закончить; 0 - продолжить восстановление:\n')
    if cont == '1':
        return matrix
    return corr(matrix)


def appr(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] is None:
                s = 0
                c = 0
                if i - 1 >= 0 and matrix[i - 1][j] is not None:
                    s += matrix[i - 1][j]
                    c += 1
                if j - 1 >= 0 and matrix[i][j - 1] is not None:
                    s += matrix[i][j - 1]
                    c += 1
                if i + 1 < n and matrix[i + 1][j] is not None:
                    s += matrix[i + 1][j]
                    c += 1
                if j + 1 < n and matrix[i][j + 1] is not None:
                    s += matrix[i][j + 1]
                    c += 1
                if c > 0:
                    matrix[i][j] = int(s / c)
    return matrix


def analitics(matrix0, matrix2, matrix3):
    sum2 = 0
    sum3 = 0
    n = len(matrix0)
    for i in range(n):
        for j in range(n):
            sum2 += abs(matrix0[i][j] - (matrix2[i][j] if matrix2[i][j] is not None else 0))
            sum3 += abs(matrix0[i][j] - (matrix3[i][j] if matrix3[i][j] is not None else 0))
    return sum2, sum3


matrix0, matrix1 = create_tale()
print('Исходная таблица')
print_table(matrix0)
print('\nТаблица с 10 удаленными значениями')
print_table(matrix1)
matrix2 = corr(copy.deepcopy(matrix1))
print('\nДо')
print_table(matrix0)
print('\nПосле')
print_table(matrix2)
matrix3 = appr(matrix1)
print('\nПосле линейной аппроксимации')
print_table(matrix3)
s1, s2 = analitics(matrix0, matrix2, matrix3)
print('\n', s1, s2)
