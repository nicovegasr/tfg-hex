import pandas as pd
from dash import html, dcc


def visualizer(files: list[pd.DataFrame]):
    layout = html.Div(
        children=[
            dcc.Graph(
                id="graph",
                config={"edits": {"legendPosition": True}},
                style={"width": "80%"},
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            "passenger_threshold",
                            dcc.Slider(0, 20, 2, value=10, id="passenger_threshold"),
                            "max_km_h",
                            dcc.Slider(5, 35, 2, value=17, id="max_km_h"),
                            "ratio_time_pass_thres",
                            dcc.Slider(
                                0, 400, 20, value=200, id="ratio_time_pass_thres"
                            ),
                            "tmax",
                            dcc.Slider(
                                5 * 60, 3600 * 1.5, 5 * 60, value=45 * 60, id="tmax"
                            ),
                            "segs_parada",
                            dcc.Slider(0, 60, 3, value=30, id="segs_parada"),
                        ]
                    ),
                    html.Div(
                        id="line_information",
                        children=[],
                        style={
                            "display": "grid",
                            "grid-template-columns": "auto auto auto auto",
                        },
                    ),
                ],
                style={"width": "20%"},
            ),
        ],
        style={
            "display": "inline-flex",
            "position": "relative",
            "width": "100%",
            "height": "500px",
        },
    )
    return [layout]
