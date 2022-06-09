import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from datetime import datetime
from fpdf import FPDF


def google_table(m, v, s):
    # https://docs.google.com/spreadsheets/d/1ucR-ZxJ8MmW26QvipwZN0o2-OrQOUhkKcpLS0vvHoM0/edit?usp=sharing
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('python-341913-2d5e4a16dd7e.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("Python").sheet1
    wks.update('A1', s)
    wks.update('B1', datetime.today().strftime('%Y-%m-%d'))
    wks.update('B4', m)
    wks.update('B5', v)

    create_pdf(wks.get_all_values(), datetime.today().strftime('%Y-%m-%d') + ' - ' + s)


def create_pdf(text, filename):
    font_size_pt = 14
    font_size_mm = font_size_pt * 0.5

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=14)
    pdf.add_page()
    pdf.set_font(family='Times', size=font_size_pt)

    for line in text:
        if len(line) == 0:
            pdf.ln()
        else:
            pdf.cell(0, font_size_mm, '   '.join(line), ln=1)

    pdf.output('pdfs/' + filename + '.pdf', 'F')


app = Dash(__name__)

app.layout = html.Div([
    html.P('Расчет кинетической энергии\n', style={'margin-bottom': 0}),
    dcc.Input(
        id='input_n',
        placeholder="масса",
        type='number',
        style={'width': 115},
        min=1
    ),
    dcc.Input(
        id='input_m',
        placeholder="скорость",
        type='number',
        style={'width': 115},
        min=1
    ),
    html.Br(),
    dcc.Input(
        id='input_s',
        placeholder="название файла",
        style={'width': 230},
    ),
    html.Br(),
    html.Button('Рассчитать', id='get_res', n_clicks=0),
    html.Div(id='res'),
])


@app.callback(
    Output('res', 'children'),
    Input('get_res', 'n_clicks'),
    State('input_n', 'value'),
    State('input_m', 'value'),
    State('input_s', 'value')
)
def update_output(_, input_n, input_m, input_s):
    if input_n and input_m and input_s:
        try:
            google_table(input_n, input_m, input_s)
            return 'Файл сохранен'
        except ValueError:
            return 'Ошибка'
    return 'Введите значения'


if __name__ == '__main__':
    app.run_server(debug=True)
