from datetime import datetime


def get_data(res, start, end, f):
    format1 = '%d.%m.%Y'
    format2 = '%Y-%m-%d'
    first = 0
    last = len(res) - 1
    arr1 = []
    for i in f.readlines():
        a = i.split('\t')
        num = a[1].replace('\n', '').replace(' ', '').replace(',', '.')
        if num and (datetime.strptime(a[0], format1) >= datetime.strptime(start, format2)) and (
                datetime.strptime(a[0], format1) <= datetime.strptime(end, format2)):
            arr1.append([datetime.strptime(a[0], format1), float(num)])
        elif num and len(arr1) == 0:
            last = [datetime.strptime(a[0], format1), float(num)]
        elif num and len(arr1) > 0 and first == 0:
            first = [datetime.strptime(a[0], format1), float(num)]
    arr1.reverse()

    a_days = (arr1[0][0] - datetime.strptime(start, format2)).days
    if a_days > 1:
        res.append(first[1])
        for j in range(1, a_days):
            res.append(None)

    res.append(arr1[0][1])
    for i in range(1, len(arr1)):
        a_days = (arr1[i][0] - arr1[i - 1][0]).days
        if a_days > 1:
            for j in range(1, a_days):
                res.append(None)
            res.append(arr1[i][1])
        else:
            res.append(arr1[i][1])

    a_days = (datetime.strptime(end, format2) - arr1[-1][0]).days
    if a_days > 1:
        for j in range(1, a_days):
            res.append(None)
        res.append(last[1])

    return res, []


def recovery(res, type_recovery):
    def winzoning(a):
        for i in range(1, len(a)):
            if a[i] is None:
                a[i] = a[i - 1]
        return a

    def appr(a):
        count = 0
        for i in range(1, len(a)):
            if a[i] is None:
                count += 1
            elif count > 0:
                for j in range(count):
                    a[i - count + j] = a[i - count + j - 1] + (a[i] - a[i - count - 1]) / (count + 1)
                count = 0
        return a

    res2 = []
    if type_recovery == 'винзорирование':
        res2 = winzoning(res)
    if type_recovery == 'линейная аппроксимация':
        res2 = appr(res)
    return res2


def smoothing(res, type_smoothing, max_deviation):
    def window_smoothing():
        res2 = [[0.0], [res[0]]]
        start = res[0]
        summ = res[0]
        countt = 1
        maxs = []
        for i in range(1, len(res)):
            if abs(res[i] - start) < max_deviation:
                summ += res[i]
                countt += 1
            else:
                res2[0].append(i - countt / 2)
                res2[1].append(summ / countt)
                maxs.append(abs(res[i] - start))
                summ = res[i]
                countt = 1
                start = res[i]
        res2[0].append(len(res) - 1)
        res2[1].append(res[-1])

        return res2, round(max(maxs), 3)

    def avg_smoothing():
        res2 = [[0.0], [res[0]]]
        maxs = []
        for i in range(1, len(res)):
            s = 0
            s2 = 0
            for j in range(min(i, max_deviation)):
                s += res[i - j] * (max_deviation - j + 1)
                s2 += (max_deviation - j + 1)
            res2[0].append(i)
            res2[1].append(s / s2)
            maxs.append(abs(res[i] - res2[1][i]))
        return res2, round(max(maxs), 3)

    if type_smoothing == 'метод скользящего среднего со скользящим окном наблюдения':
        return window_smoothing()

    if type_smoothing == 'взвешенный метод скользящего среднего':
        return avg_smoothing()


def main(companies, start, end, type_recovery, type_smoothing, max_deviation):
    res = []
    with open('companies/' + companies + '.txt', encoding='utf-8') as f:
        res, dates = get_data(res, start, end, f)
    res = recovery(res, type_recovery)
    res2, max_deviation_res = smoothing(res, type_smoothing, max_deviation)
    return res, res2, max_deviation_res
