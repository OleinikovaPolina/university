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
