**Задача №1**

Задание. Используя результаты из задания 6 лабораторной работы №1 создать модуль, позволяющий производить возведение в квадрат, транспонирование и нахождение определителя матрицы. Подключить данный модуль к новой программе. Проверить быстродействие реализованных функций. Реализовать аналогичные функции с помощью модуля NumPy. Сравнить быстродействие. Постараться улучшить результат. Исходная и улучшенная версия алгоритмов должна быть отражена на GitHub (https://github.com/OleinikovaPolina/1kurs/tree/main/Python-Programming/Lab-2).

Решение.

```py
import copy


class Matrix:
    def __init__(self, matrix):
        self.n = len(matrix)
        self.m = len(matrix[0])
        self.matrix = matrix

    @staticmethod
    def get_minor(matrix, i, j):
        minor = copy.deepcopy(matrix)
        del minor[i]
        for i in range(len(matrix[0]) - 1):
            del minor[i][j]
        return minor

    def det(self, matrix=None):
        if not matrix:
            matrix = self.matrix
        if len(matrix) != len(matrix[0]):
            return None
        if len(matrix[0]) == 1:
            return matrix[0][0]
        signum = 1
        determinant = 0
        for j in range(len(matrix[0])):
            determinant += matrix[0][j] * signum * self.det(self.get_minor(matrix, 0, j))
            signum *= -1
        return determinant

    def squaring(self):
        if self.n != self.m:
            return None
        new_matrix = []
        for i in range(self.n):
            new_matrix.append([])
        for i in range(self.n):
            for j in range(self.n):
                new_matrix[i].append(0)
                for k in range(self.n):
                    new_matrix[i][j] += self.matrix[i][k] * self.matrix[k][j]
        return new_matrix

    def transposition(self):
        new_matrix = [[self.matrix[j][i] for j in range(self.n)] for i in range(self.m)]
        return new_matrix

    def max(self):
        return max(map(max, self.matrix))

    def __str__(self):
        return '\n'.join(
            [' '.join(
                map(lambda x: '{}{}'.format((len(str(self.max())) - len(str(x))) * ' ', x), i))
                for i in self.matrix
            ])
```

Пояснение. В программе представлен модуль из 1 лабораторной работы. В программе создан класс матрицы с функциями транспонирования, нахождения детерминанта, возведения в квадрат, нахождения максимума (для вывода матрицы), взятия минора (для нахождения детерминанта).

```py
import time
import numpy as np
from module_for_1 import Matrix

n, m = map(int, input('Введите размеры матрицы n m\n').split())
print('Введите построчно матрицу, разделяя значения пробелами\n')
a = []
for i in range(n):
    a.append([float(j) for j in input().split()])
a1 = Matrix(a)
a2 = np.array(a)

time_start = time.perf_counter()
print('NumPy нахождение детерминанта \nРезультат ', np.linalg.det(a2))
print('Время ', time.perf_counter() - time_start)

time_start = time.perf_counter()
print('\nNumPy возведение в квадрат \nРезультат  \n', np.linalg.matrix_power(a2, 2))
print('Время ', time.perf_counter() - time_start)

time_start = time.perf_counter()
print('\nNumPy транспонирование \nРезультат  \n', a2.transpose())
print('Время ', time.perf_counter() - time_start)


print('\nСвой модуль нахождение детерминанта \nРезультат')
time_start = time.perf_counter()
print(a1.det())
print('Время ', time.perf_counter() - time_start)

print('\nСвой модуль возведение в квадрат \nРезультат')
time_start = time.perf_counter()
print(Matrix(a1.squaring()))
print('Время ', time.perf_counter() - time_start)

print('\nСвой модуль транспонирование \nРезультат')
time_start = time.perf_counter()
print(Matrix(a1.transposition()))
print('Время ', time.perf_counter() - time_start)

```

Пояснение. В программе с консоли считывается матрица. После с помощью модуля numpy и своего производятся доступные действия и выводится результат и время работы.

Результат работы программы отображен на рисунке 1.

```
Введите размеры матрицы n m
3 3
Введите построчно матрицу, разделяя значения пробелами

1 2 3
4 5 6
7 8 9
NumPy нахождение детерминанта 
Результат  0.0
Время  0.005998699999999246

NumPy возведение в квадрат 
Результат  
 [[ 30.  36.  42.]
 [ 66.  81.  96.]
 [102. 126. 150.]]
Время  0.0005822000000001992

NumPy транспонирование 
Результат  
 [[1. 4. 7.]
 [2. 5. 8.]
 [3. 6. 9.]]
Время  0.001614600000001687

Свой модуль нахождение детерминанта 
Результат
0.0
Время  0.0001391999999995619

Свой модуль возведение в квадрат 
Результат
 30.0  36.0  42.0
 66.0  81.0  96.0
102.0 126.0 150.0
Время  8.19999999990273e-05

Свой модуль транспонирование 
Результат
1.0 4.0 7.0
2.0 5.0 8.0
3.0 6.0 9.0
Время  4.020000000082291e-05
```
Рисунок 1 – Результат работы программы

Пояснение. С помощью модуля numpy [1] и своего производятся доступные действия с матрицей 2 на 2 и выводится результат и время работы.

Вывод . Вывод матрицы у модулей различается. У своего лучше отсутствие скобок, но хуже присутствие &quot;,0&quot;. Время работы своего модуля, конечно, больше, но для действий пользователя вполне нормальное. На маленьких матрицах такая разница даже не заметна. В итоге можно сказать, что был создан модуль для простейших действий с матрицами, была повторена работа с модулем numpy.

**Задача №2**

Задание. Создать таблицу nxn, заполненную случайными величинами в диапазоне от 1 до 30. Удалить значения из 10 случайных ячеек. Реализовать алгоритм, восстанавливающий данные путем линейной аппроксимации. Реализовать алгоритм, восстанавливающий значения путем корреляционного восстановления. Коррелируемые между собой ряды измерений выбирает пользователь при запуске программы. Проанализироватьдостоинстваинедостаткиметодоввосстановленияданных.

Решение.

```py
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

```


Пояснение. В программе представлено много функций.

- liner\_fitting: представляет собой реализацию алгоритм метода наименьших квадратов;
- Calculate: находит значения для удаленного элемента;
- print\_table: записывает таблицу с наименованием столбцов и строк;
- create\_tale: cоздает таблицу nxn, заполненную случайными величинами в диапазоне от 1 до 30. Удаляет значения из 10 случайных ячеек;
- get\_rows: берет строки или столбцы для корреляции после ответа пользователся
- set\_rows: вписывает результат в тблицу с удаленными значениями;
- corr: для корреляции;
- appr: для линейной аппроксимации;
- analitics: подсчитывает сумму разниц между удаленными и получившимися значениями по модулю;
- for\_corrcoef, corrcoef: считает коэффициенты Пирсона [2] и выводит их.

Результат работы программы отображен на рисунке 2.
```
Введите n>3
7
Исходная таблица
       0c   1c   2c   3c   4c   5c   6c
  0r   30   27   17   21    1   21    4
  1r    4   12    3   21   10    9   23
  2r   22   11   20   18   23    4   30
  3r    3    5   29   12   29   21    1
  4r   22   21    1    2   23    9    5
  5r   13   11   28   25   30   19    9
  6r   18    9   10   15   10   15    9

Таблица с 10 удаленными значениями
       0c   1c   2c   3c   4c   5c   6c
  0r   30   27   17 None    1 None    4
  1r    4   12    3 None   10 None   23
  2r   22   11   20   18   23    4   30
  3r    3    5   29   12 None   21    1
  4r   22   21 None    2 None    9 None
  5r   13   11   28 None   30   19    9
  6r   18    9   10 None   10   15    9

Коэффициенты корреляции Пиросна (Если убрать Nones)
          0r      1r      2r      3r      4r      5r      6r
  0r +1.0000 -0.5344 -0.6555 -0.0412 +1.0000 -0.3990 +0.5683
  1r -0.5344 +1.0000 +0.4453 -0.5965 -1.0000 -0.5352 -0.5318
  2r -0.6555 +0.4453 +1.0000 -0.4205 +0.1932 -0.0329 -0.2664
  3r -0.0412 -0.5965 -0.4205 +1.0000 -0.7172 +0.9667 -0.0334
  4r +1.0000 -1.0000 +0.1932 -0.7172 +1.0000 -0.9518 -0.1207
  5r -0.3990 -0.5352 -0.0329 +0.9667 -0.9518 +1.0000 -0.1348
  6r +0.5683 -0.5318 -0.2664 -0.0334 -0.1207 -0.1348 +1.0000

Коэффициенты корреляции Пиросна (Если убрать Nones)
          0c      1c      2c      3c      4c      5c      6c
  0c +1.0000 +0.7638 -0.0225 -0.1429 -0.3144 -0.8674 +0.0235
  1c +0.7638 +1.0000 -0.2081 -0.7245 -0.6355 -0.5597 -0.1192
  2c -0.0225 -0.2081 +1.0000 -1.0000 +0.6621 +0.4376 -0.4291
  3c -0.1429 -0.7245 -1.0000 +1.0000 None +1.0000 +1.0000
  4c -0.3144 -0.6355 +0.6621 None +1.0000 +0.0888 +0.3427
  5c -0.8674 -0.5597 +0.4376 +1.0000 +0.0888 +1.0000 -0.9753
  6c +0.0235 -0.1192 -0.4291 +1.0000 +0.3427 -0.9753 +1.0000
  
Введите ряды
0c 5c
       0c   1c   2c   3c   4c   5c   6c
  0r   30   27   17 None    1    2    4
  1r    4   12    3 None   10   22   23
  2r   22   11   20   18   23    4   30
  3r    3    5   29   12 None   21    1
  4r   22   21 None    2 None    9 None
  5r   13   11   28 None   30   19    9
  6r   18    9   10 None   10   15    9

Введите 1, если хотите закончить; 0 - продолжить восстановление:
0
...
Введите 1, если хотите закончить; 0 - продолжить восстановление:
1

До
       0c   1c   2c   3c   4c   5c   6c
  0r   30   27   17   21    1   21    4
  1r    4   12    3   21   10    9   23
  2r   22   11   20   18   23    4   30
  3r    3    5   29   12   29   21    1
  4r   22   21    1    2   23    9    5
  5r   13   11   28   25   30   19    9
  6r   18    9   10   15   10   15    9

После
       0c   1c   2c   3c   4c   5c   6c
  0r   30   27   17  -12    1    2    4
  1r    4   12    3    9   10   22   23
  2r   22   11   20   18   23    4   30
  3r    3    5   29   12 None   21    1
  4r   22   21   16    2    8    9    9
  5r   13   11   28   10   30   19    9
  6r   18    9   10   13   10   15    9

После линейной аппроксимации
       0c   1c   2c   3c   4c   5c   6c
  0r   30   27   17    9    1    2    4
  1r    4   12    3   10   10    9   23
  2r   22   11   20   18   23    4   30
  3r    3    5   29   12   18   21    1
  4r   22   21   20    2   14    9    6
  5r   13   11   28   20   30   19    9
  6r   18    9   10   13   10   15    9

 157 89
```

Рисунок 2 – Результат работы программы

Пояснение. Представлен результат работы программы для n=7(взята только часть)

Вывод . Так как с восстановлением данных я столкнулась впервые, то реализовала все что нашла по теме. По результатам работы, проведя несколько тестов выяснилось, что линейная аппроксимация в данном случае удачней. Думаю, это потому, что там считается среднее значение между значениями из маленького промежутка (1, 30). Поэтому независимо от количества n результат будет примерно с одной точностью. Насчет корреляции. Здесь все зависит от выбора пользователя. Если он будет правильно учитывать коэффициент Пирсона, то значение analytics будет около 150. Если нет – в несколько тысяч (когда корреляции не будет или будет слишком слабая). Ну и стоит учитывать, что у нас все-таки значения рандомные, что не гарантирует хороший результат. Также было замечено, что при маленьком n результат становится хуже (так как коррелировать почти нечего из-за множества None).

**Задача №3**

Задание. Создать таблицу nxn, заполненную случайными величинами в диапазоне от 1 до 30. Реализовать алгоритм поиска математического ожидания и дисперсии для каждого из рядов созданной таблицы.

Решение. 

```py
import random

n = int(input('Введите n\n'))
matrix = [[random.randint(1, 30) for j in range(n)] for i in range(n)]
for lst in matrix:
    print('\nРяд: ', *lst)
    avg = sum(lst) / len(lst)
    print('математическое ожидание: ', avg)
    var = sum((x - avg) ** 2 for x in lst) / len(lst)
    print('дисперсия: ', var)

```

Пояснение. В программе создается матрица заполненная рандомными значениями, считается математическое ожидание и дисперсия для каждого ряда.

Результат работы программы отображен на рисунке 3.
```
Введите n
5

Ряд:  11 13 28 15 7
математическое ожидание:  14.8
дисперсия:  50.559999999999995

Ряд:  13 17 28 7 28
математическое ожидание:  18.6
дисперсия:  69.03999999999999

Ряд:  9 18 27 11 24
математическое ожидание:  17.8
дисперсия:  49.36

Ряд:  16 5 22 3 23
математическое ожидание:  13.8
дисперсия:  70.16

Ряд:  17 17 6 30 29
математическое ожидание:  19.8
дисперсия:  78.96000000000001
```

Рисунок 3 – Результат работы программы

Пояснение. Представлен результат работы программы для n=3

Вывод . В результате работы был создан алгоритм, считающий математическое ожидание и дисперсию. Если посчитать среднее значения получившихся результатов, то можно сделать вывод о том, что при увеличении n мат ожидание будет стремиться к 15, а дисперсия к 75.

**СПИСОК ЛИТЕРАТУРЫ**

1. NumPy. NumPy documentation. [Электронный ресурс] – https://numpy.org/doc/stable/(09.03.2022);
2. Распознавание. Коэффициент корреляции Пирсона. [Электронный ресурс] – [www.machinelearning.ru/wiki/index.php?title=Коэффициент\_корреляции\_Пирсона](http://www.machinelearning.ru/wiki/index.php?title=%D0%9A%D0%BE%D1%8D%D1%84%D1%84%D0%B8%D1%86%D0%B8%D0%B5%D0%BD%D1%82_%D0%BA%D0%BE%D1%80%D1%80%D0%B5%D0%BB%D1%8F%D1%86%D0%B8%D0%B8_%D0%9F%D0%B8%D1%80%D1%81%D0%BE%D0%BD%D0%B0) (09.03.2022);