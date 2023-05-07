import json
from dash import html, dcc, callback, Input, Output
from infrastructure.http_requesters.algorithm_http_requester import AlgorithmHttpRequester


def dropdown_component() -> html:
    try:
        algorithm_availables_request = AlgorithmHttpRequester.get_available_algorithms()
        if (algorithm_availables_request.status_code != 200):
            error = algorithm_availables_request.content.decode('utf-8')
            return html.P(className="dropdown-error", children=error)
        algorithm_availables = json.loads(algorithm_availables_request.content.decode('utf-8'))
        return dcc.Dropdown(id='dropdown-selection', options=algorithm_availables, placeholder="Seleccione un algoritmo.", clearable=False)
    except:
        return html.P(className="dropdown-error", children="There is a problem with server conexion.")

@callback(
    [Output('description', 'children'),
     Output('algorithm_selected', 'data'),
     Output('description', 'style')],
    Input('dropdown-selection', 'value')
)
def description(algorithm_selected: str) -> list[html.Div, str, dict]:
    if algorithm_selected is None:
        return [None, {'data': None}, {'visibility': 'hidden'}]
    description = AlgorithmHttpRequester.get_algorithm_description(algorithm_selected)
    if description.status_code != 200:
        error = description.content.decode('utf-8')
        error_component = html.Div(className='descripcion-error', children=[error])
        return [error_component, {'data': algorithm_selected}, {'visibility': 'visible'}]
    description = json.loads(description.content.decode('utf-8'))
    description_component = (
        html.P(className="descripcion-titulo", children=["Has seleccionado el algoritmo: ", html.Span(className='descripcion-valor', children=algorithm_selected + '.')]),\
        html.Div(className='descripcion-cuerpo', children=[html.Li(children=[description[0]]), html.Li(children=[description[1]])]),\
        html.Div(className='files', children=[
            dcc.Upload(className='upload-file', id={'type': 'upload-file', 'index': 'upload'}, multiple=True, children=[html.A(
                 children='Arrastra o selecciona un archivo.')]),
            html.Div(className="upload-message",
                     id="upload-message", children='')
        ]))
    return [description_component, {'data': algorithm_selected}, {'visibility': 'visible'}]
