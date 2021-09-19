import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from data_handler import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


row = html.Div([
    dbc.Row(dbc.Col(html.H1(children=["COVID-19 Dashboard"]), width={"size": 6, "offset": 4} )),
    dbc.Row([
        dbc.Col(Dropdown(
            id="province",
            options=[{"label": x, "value": x}
                     for x in ['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'total']],
            value='total',
            clearable=False
        ), width=4),
        ]),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id="confirmed" ), width=6),
            dbc.Col(dcc.Graph(id="daily_confirmed"), width=6),

        ]
    ),
    dbc.Row(
    [
        dbc.Col(dcc.Graph(id="deaths" ), width=6),
        dbc.Col(dcc.Graph(id="daily_deaths"), width=6),

    ]
),
])


app.layout = html.Div(row) 


@app.callback(
    Output("confirmed", "figure"),
    [Input("province", "value")]
)
def show_province(province):
    data = get_covid19_data(["confirmed"])

    df = to_long_form(data["confirmed"]["data"])
    df_mod = df.loc[df["variable"] == province]
    return px.line(df_mod, x="date", y="value", color="variable")

@app.callback(
    Output("daily_confirmed", "figure"),
    [Input("province", "value")]
)
def show_daily_cases(province):
    data = get_covid19_data(["confirmed"])

    df = to_long_form(data["confirmed"]["data"])
    df_mod = df.loc[df["variable"] == province]
    df_mod['daily'] = df_mod["value"].diff()
    df_mod["rolling"] = df_mod['daily'].rolling(window=7).mean()
    fig = px.line(df_mod, x="date", y="rolling", color="variable")
    fig.add_bar(x=df_mod["date"], y=df_mod["daily"])
    return fig

@app.callback(
    Output("deaths", "figure"),
    [Input("province", "value")]
)
def show_province(province):
    data = get_covid19_data(["deaths"])

    df = to_long_form(data["deaths"]["data"])
    df_mod = df.loc[df["variable"] == province]
    return px.line(df_mod, x="date", y="value", color="variable")

@app.callback(
    Output("daily_deaths", "figure"),
    [Input("province", "value")]
)
def show_daily_cases(province):
    data = get_covid19_data(["deaths"])

    df = to_long_form(data["deaths"]["data"])
    df_mod = df.loc[df["variable"] == province]
    df_mod['daily'] = df_mod["value"].diff()
    df_mod["rolling"] = df_mod['daily'].rolling(window=7).mean()
    fig = px.line(df_mod, x="date", y="rolling", color="variable")
    fig.add_bar(x=df_mod["date"], y=df_mod["daily"])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
