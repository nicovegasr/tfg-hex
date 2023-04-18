import dash
from dash import html, dcc
from src.infrastructure.app.components.dropdown import dropdown_component
from src.infrastructure.app.components.uploadfiles import *

dash.register_page(__name__, path='/', title='Inicio')

layout = html.Div(className="global", children=[
    html.Div(className="zona1", children=[
        html.Div(className="algoritmos", children=[
            html.P(className="algoritmos-tittle",
                   children='Selección de algoritmo.'),
            html.Div(className='select-algoritmo', children=[
                dropdown_component()
            ]),
        ]),
        html.Div(id='description'),
    ]),
    html.Div(id="resultado"),
    html.Div(id="visualizacion", className="visualizacion"),
    dcc.Download(id="descarga"),
    dcc.Store(id="algorithm_selected"),
    html.P(id="no-output")

])
