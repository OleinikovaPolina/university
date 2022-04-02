from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from datetime import date, timedelta, datetime
from module import main
import plotly.graph_objs as go
import math

companies = ['алроса', 'афк', 'аэрофлот', 'втб', 'газпром', 'ленэнерго', 'лср', 'лукойл', 'мосбиржа', 'мтс', 'нлмк',
             'новатэк', 'пик', 'русгидро', 'сбер', 'северсталь', 'татнефть', 'яндекс']

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(companies, 'алроса', id='company', placeholder='Тикер', style={'width': '265px'}),
    dcc.DatePickerSingle(id='start', date=date(2016, 12, 1), min_date_allowed=date(2016, 12, 1),
                         max_date_allowed=date(2019, 12, 31), placeholder='Начало', ),
    dcc.DatePickerSingle(id='end', date=date(2019, 12, 31), min_date_allowed=date(2016, 12, 1),
                         max_date_allowed=date(2019, 12, 31), placeholder='Конец', ),
    dcc.Dropdown(['винзорирование', 'линейная аппроксимация'], 'линейная аппроксимация', id='type_recovery',
                 placeholder='Метод восстановления', style={'width': '265px'}),
    dcc.Dropdown(
        ['взвешенный метод скользящего среднего', 'метод скользящего среднего со скользящим окном наблюдения'],
        'метод скользящего среднего со скользящим окном наблюдения', id='type_smoothing',
        placeholder='Метод сглажтивания', style={'width': '265px'}),
    dcc.Input(1, id="max_deviation", type="number", placeholder='Окно',
              style={'width': '265px'}),
    html.Br(),
    html.Button('Build', id='submit-val', n_clicks=0),
    dcc.Graph(id='graph-with-slider'),
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('company', 'value'),
    State('start', 'date'),
    State('end', 'date'),
    State('type_recovery', 'value'),
    State('type_smoothing', 'value'),
    State('max_deviation', 'value'),
)
def update_output(n_clicks, company, start, end, type_recovery, type_smoothing, max_deviation):
    text = 'Результат'
    if company is None:
        text = 'Выберите компанию'
    if start is None:
        text = 'Выберите дату начала'
    if end is None:
        text = 'Выберите дату окончания'
    if type_recovery is None:
        text = 'Выберите метод восстановления'
    if type_smoothing is None:
        text = 'Выберите метод сглаживания'
    if max_deviation is None:
        text = 'Выберите максимальное отклонение сглаживающего процесса'
    if text != 'Результат':
        fig = go.Figure(layout={'title': text})
        fig.update_layout(transition_duration=500)
        return fig
    try:
        old, new, maxs = main(company, start, end, type_recovery, type_smoothing, max_deviation)
        dates1 = [(datetime.strptime(start, '%Y-%m-%d') + timedelta(days=i)).strftime('%d.%m.%Y') for i in
                  range(0, (datetime.strptime(end, '%Y-%m-%d') - datetime.strptime(start, '%Y-%m-%d')).days + 1)]
        dates2 = []
        for i in new[0]:
            dates2.append(dates1[math.floor(i)])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates1, y=old, name='before'))
        fig.add_trace(go.Scatter(x=dates2, y=new[1], name='after'))
        fig.update_layout(title_text=f'Результат (максимально отклонение = {maxs} )')
    except ValueError:
        fig = go.Figure()
        fig.update_layout(title_text='Уменьшите максимальное отклонение или увеличьте период')

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
    
