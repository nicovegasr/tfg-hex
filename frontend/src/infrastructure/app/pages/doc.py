import dash
from dash import dcc, html

dash.register_page(__name__, path="/doc", title="Documentacion")

layout = html.Div(
    className="conductores",
    children=[
        html.Div(
            className="conductores-text-1",
            children=[
                html.Video(src="/static/my-video.mov", controls=True),
                dcc.Markdown(
                    """
            # Instrucciones para añadir algoritmos.
            
            """
                ),
            ],
        )
    ],
)
