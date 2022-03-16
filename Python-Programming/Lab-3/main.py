import math
from datetime import datetime
import numpy


def getData():
    format = '%d.%m.%Y'
    arr1 = []
    arr2 = []
    for i in f.readlines():
        a = i.split('\t')
        num = a[1].replace('\n', '').replace(' ', '').replace(',', '.')
        if num:
            arr1.append(
                [datetime.strptime(a[0], format), float(num)])
    arr1.reverse()
    arr2.append(arr1[0][1])
    for i in range(1, len(arr1)):
        a_days = (arr1[i][0] - arr1[i - 1][0]).days
        if a_days > 1:
            for j in range(1, a_days):
                new_var = arr1[i - 1][1] + (arr1[i][1] - arr1[i - 1][1]) / a_days * j
                arr2.append(round(new_var, 3))
            arr2.append(arr1[i][1])
        else:
            arr2.append(arr1[i][1])
    arr2.append(arr1[-1][1])
    return arr2


def getMaxMin(arr):
    corr = numpy.corrcoef(arr)
    for i in corr:
        print(*[round(j, 3) for j in i], file=fCorrCoref)
    max = [[0]] * 3
    min = [[math.inf]] * 3
    for i in range(len(corr)):
        for j in range(i + 1, len(corr[i])):
            if corr[i][j] > max[0][0] and arr[i][-1] - arr[i][0] > 0 and arr[j][-1] - arr[j][0] > 0:
                max.append([corr[i][j], i, j])
                max.sort(key=lambda x: x[0])
                max.pop(0)
            if abs(corr[i][j]) < abs(min[0][-1]) and arr[i][-1] - arr[i][0] > 0 and arr[j][-1] - arr[j][0] > 0:
                min.append([abs(corr[i][j]), i, j, corr[i][j]])
                min.sort(key=lambda x: x[0])
                min.pop()
    return [max, min]


def forTB(arr, p, s, type):
    f = fTolya if type == 0 else fBorya
    x = 0
    cc = 0
    for i in p:
        if len(i) > 1:
            cc += 1
            print(f'{cc} пара с коэф: {i[0]}', file=f)
            com1 = (s // arr[i[1]][0]) * arr[i[1]][-1]
            print(
                f'Компания: {company[i[1]]} Акция стоила: {arr[i[1]][0]} Акция стоит: {arr[i[1]][-1]} Количество купленного: {(s // arr[i[1]][0])} Продали: {com1}',
                file=f)
            com2 = (s // arr[i[2]][0]) * arr[i[2]][-1]
            print(
                f'Компания: {company[i[2]]} Акция стоила: {arr[i[2]][0]}Акция стоит: {arr[i[2]][-1]} Количество купленного: {(s // arr[i[2]][0])} Продали: {com2}',
                file=f)
            x = x + com1 + com2
    print(f'Получившаяся сумма: {round(x, 3)}', file=f)
    return x


def Tolya(arr, p):
    global sumTolya
    c = 0
    for i in p:
        if len(i) > 1:
            c += 2
    s = sumTolya / c
    x = forTB(arr, p, s, 0)
    if x != 0:
        sumTolya = x


def Borya(arr, p):
    global sumBorya
    c = 0
    for i in p:
        if len(i) > 1:
            c += 2
    s = sumBorya / c
    x = forTB(arr, p, s, 1)
    if x != 0:
        sumBorya = x


def Zhenya(arr):
    global sumZhenya
    sum = 0
    s = sumZhenya
    x = 0
    for i in range(len(arr)):
        sum += arr[i][0]
    for i in range(len(arr)):
        com = ((arr[i][0] / sum * s) // arr[i][0]) * (arr[i][-1])
        print(
            f'Компания: {company[i]} Акция стоила: {arr[i][0]} Акция стоит: {arr[i][-1]} Количество купленного: {(arr[i][0] / sum * s) // arr[i][0]} Продали: {com}',
            file=fZhenya)
        x += com
    print(f'Получившаяся сумма: {round(x, 3)}', file=fZhenya)
    sumZhenya = x


# детский мир, полиметалл
company = ['алроса', 'афк', 'аэрофлот', 'втб', 'газпром', 'ленэнерго', 'лср', 'лукойл', 'мосбиржа',
           'мтс', 'нлмк', 'новатэк', 'пик', 'русгидро', 'сбер', 'северсталь', 'татнефть', 'яндекс']
res = []
for i in range(len(company)):
    with open('2/' + company[i] + '.txt', encoding='utf-8') as f:
        res.append(getData())
sumTolya = 10 ** 7
sumBorya = 10 ** 7
sumZhenya = 10 ** 7
fTolya = open('Tolya.txt', 'w', encoding='utf-8')
fBorya = open('Borya.txt', 'w', encoding='utf-8')
fZhenya = open('Zhenya.txt', 'w', encoding='utf-8')
fCorrCoref = open('CorrCoref.txt', 'w', encoding='utf-8')

# first
newarr = []
for j in range(len(res)):
    newarr.append(res[j][0:31])
    res[j] = res[j][31:len(res[j])]
params = getMaxMin(newarr)
# other
s = 0
for z in range(3):
    l = 0
    for i in range(4):
        coff = 0
        for k in range(l, l + 3):
            coff += 28 if k == 2 else 30 if k in [4, 6, 9, 11] else 31
        newarr = []
        for j in range(len(res)):
            newarr.append(res[j][0:coff])
            res[j] = res[j][coff:len(res[j])]
        strYQ = f'\n{2017 + z}-й год {i + 1}-й квартал'
        print(strYQ, file=fTolya)
        print(strYQ, file=fBorya)
        print(strYQ, file=fZhenya)
        print(strYQ, file=fCorrCoref)
        Tolya(newarr, params[1])
        Borya(newarr, params[0])
        Zhenya(newarr)
        params = getMaxMin(newarr)
        l += 3
# 6
# 10815545.54
# 16856234.33
# 15472722.72
# 3
# 16953445.3
# 15010368.9
# 15429422.19
