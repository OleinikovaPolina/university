from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import os
import webbrowser

directory = 'C:/Users/olein/Desktop/Учеба/Программирование/hw6/pdfs/'


def get_files():
    dir_name = 'pdfs'
    files = os.listdir(dir_name)
    options = []
    for file in files:
        options.append({'label': " - ".join(file.split(' - ')[1:]), 'value': file})
    return options


app = Dash(__name__)

app.layout = html.Div([
    html.P('Файлы\n'),
    dcc.Dropdown(get_files(), '', id='files'),
    html.Button('Открыть', id='get_res', n_clicks=0),
    html.Div(id='res'),
])


@app.callback(
    Output('res', 'children'),
    Input('get_res', 'n_clicks'),
    State('files', 'value')
)
def update_output(_, input_n):
    if input_n:
        webbrowser.open_new(directory + input_n)
        return ''
    return 'Выберите файл'


if __name__ == '__main__':
    app.run_server(debug=True)
