import random
import pandas as pd
import math
import matplotlib.pyplot as plt


def get_data(start, end, n, my_fun):
    x = start
    res_x = []
    res_y = []
    while x <= end:
        res_x.append(x)
        res_y.append(my_fun(x))
        x += n
    return res_x, res_y


def get_sko(data_y):
    sum_y = sum(data_y)
    len_y = len(data_y)
    avg_y = sum_y / len_y
    res = 0
    for i in range(len_y):
        res += (data_y[i] - avg_y) ** 2
    return (res / len_y) ** 0.5


def smoothing(data_y):
    sko = get_sko(data_y)
    res = [data_y[0]]
    array = [data_y[0]]
    for i in range(1, len(data_y)):
        k = True
        array.append(data_y[i])
        while k and len(array) > 1:
            new_val = sum(array) / len(array)
            if abs(new_val - data_y[i]) < sko:
                res.append(new_val)
                k = False
            else:
                del array[0]
        if k:
            res.append(array[0])
    return res


def liner_fitting(data_x, data_y):
    size = len(data_x)
    i = 0
    sum_xy = 0
    sum_y = 0
    sum_x = 0
    sum_sqare_x = 0
    while i < size:
        sum_xy += data_x[i] * data_y[i]
        sum_y += data_y[i]
        sum_x += data_x[i]
        sum_sqare_x += data_x[i] * data_x[i]
        i += 1
    average_x = sum_x / size
    average_y = sum_y / size
    return_k = (size * sum_xy - sum_x * sum_y) / (size * sum_sqare_x - sum_x * sum_x)
    return_b = average_y - average_x * return_k
    return [return_k, return_b]


def calculate(data_x, k, b):
    data_y = []
    for z in data_x:
        data_y.append(k * z + b)
    return data_y


def main(start, end, n, fun):
    data_x, data_y = get_data(start, end, n, fun)

    data_y_smooth = smoothing(data_y)

    parameter = liner_fitting(data_x, data_y_smooth)
    data_y_mnk = calculate(data_x, parameter[0], parameter[1])

    real_value = fun(data_x[-1] + n)
    predicted_value = (data_y[-1] - data_y[-2]) + data_y[-1]
    predicted_value_smooth = (data_y_smooth[-1] - data_y_smooth[-2]) + data_y_smooth[-1]
    print(real_value, predicted_value, predicted_value_smooth, abs(real_value - predicted_value),
          abs(real_value - predicted_value_smooth))

    df = pd.DataFrame({'x': data_x,
                       'y': data_y,
                       'y smoothing': data_y_smooth,
                       'y mnk': data_y_mnk})
    df.to_excel('./excel.xlsx')

    plt.plot(data_x, data_y, '-', data_x, data_y_smooth, '--', data_x, data_y_mnk, ":")
    plt.show()


# start_val, end_val, n_val = map(float, input().split())
start_val, end_val, n_val = 3.14, 18.85, 0.05
main(start_val, end_val, n_val, lambda x: math.sin(x) + 0.1 * math.sin(x ** 5))

start_val, end_val, n_val = 0, 300, 1
main(start_val, end_val, n_val,
     lambda x: math.e ** (-x / 50) * math.sin(6 * math.pi * x / 200) + random.uniform(0, 0.1) - 0.1)

start_val, end_val, n_val = 0, 30, 0.5
main(start_val, end_val, n_val, lambda x: math.sin(x) + random.uniform(0, 2) - 1)
