import dash
from dash import dcc, html

from infrastructure.app.components.btn_result import *
from infrastructure.app.components.dropdown import dropdown_component
from infrastructure.app.components.uploadfiles import *
from infrastructure.app.components.btn_download import *

dash.register_page(__name__, path="/", title="Inicio")

layout = html.Div(
    className="global",
    children=[
        html.Div(
            className="zona1",
            children=[
                html.Div(
                    className="algoritmos",
                    children=[
                        html.P(
                            className="algoritmos-tittle",
                            children="Selección de algoritmo.",
                        ),
                        html.Div(
                            className="select-algoritmo",
                            children=[dropdown_component()],
                        ),
                    ],
                ),
                html.Div(id="description"),
            ],
        ),
        html.Div(id="result"),
        html.Div(id="visualizacion", className="visualizacion"),
        dcc.Download(id="descarga"),
        dcc.Store(id="algorithm_selected"),
        dcc.Store(id="configuration_file"),
        dcc.Store(id="uploaded_files"),
        dcc.Store(id="uploaded_files_no_processed"),
    ],
)
