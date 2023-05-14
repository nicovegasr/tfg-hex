import dash
from dash import Dash, dcc, html

# Iniciamos el servidor dash con la configuracion multipaginas activada.
server = Dash(__name__, use_pages=True)
server.config.suppress_callback_exceptions = True
# En el layout principal ponemos el header y el footer que se mantendran.
# Con el dash.pge_container le decimos que tenemos varias paginas que luego settearemos en cada fichero, aplicando al home la raiz "/".
server.layout = html.Div(
    children=[
        html.Header(
            children=[
                dcc.Link("TITSA", href="/", className="header-text-1"),
                html.P(className="header-text-2", children=">◯"),
                html.P(
                    className="header-text-3", children="Trabajando por una isla unida"
                ),
            ]
        ),
        html.Footer(
            children=[
                html.P(className="footer-text-1", children="© Titsa S.A. 2022."),
                html.P(className="footer-text-2", children="Universidad de La Laguna."),
                dcc.Link("Documentacion", href="/doc", className="footer-text-3"),
            ]
        ),
        dash.page_container,
    ]
)
# Iniciamos la aplicación.
server.run_server(debug=True, host='0.0.0.0')
