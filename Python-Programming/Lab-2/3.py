import random

n = int(input('Введите n\n'))
matrix = [[random.randint(1, 30) for j in range(n)] for i in range(n)]
for lst in matrix:
    print('\nРяд: ', *lst)
    avg = sum(lst) / len(lst)
    print('математическое ожидание: ', avg)
    var = sum((x - avg) ** 2 for x in lst) / len(lst)
    print('дисперсия: ', var)
