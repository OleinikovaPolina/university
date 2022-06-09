import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from datetime import datetime


def regression_equation(data, dates):
    b = search_b(data)
    a = sum(data) / len(data) * (1 - b)
    forecast = []
    for i in data:
        forecast.append(a + b * i)

    fig, ax = plt.subplots()
    ax.plot(dates, data)
    ax.plot(dates, forecast, 'o--')
    plt.show()


def search_b(data):
    y1 = sum(data[1:]) / len(data[1:])
    y2 = sum(data[:-1]) / len(data[:-1])
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    for i in range(1, len(data)):
        numerator += (data[i] - y1) * (data[i - 1] - y2)
        denominator1 += (data[i] - y1) ** 2
        denominator2 += (data[i - 1] - y2) ** 2
    return numerator / (denominator1 * denominator2) ** 0.5


def google_table():
    # https://docs.google.com/spreadsheets/d/1ucR-ZxJ8MmW26QvipwZN0o2-OrQOUhkKcpLS0vvHoM0/edit?usp=sharing
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('python-341913-2d5e4a16dd7e.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("Python").worksheet('Лист2')

    dates = list(map(lambda o: datetime.strptime(o, '%d.%m.%Y'), wks.col_values(1)))
    y = list(map(lambda o: float(o.replace(',', '.')), wks.col_values(2)))
    regression_equation(y, dates)

    dates = list(map(lambda o: datetime.strptime(o, '%d.%m.%Y'), wks.col_values(4)))
    y = list(map(lambda o: float(o.replace(',', '.')), wks.col_values(5)))
    regression_equation(y, dates)


google_table()
