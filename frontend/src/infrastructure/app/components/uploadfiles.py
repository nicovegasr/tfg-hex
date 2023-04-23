import json
from dash import html, callback, Input, Output, ALL
from aplication.usecases.sort_uploaded_files import body_of_uploading_files

@callback(
    Output('upload-message', 'children'),
    Input({'type': 'upload-file', 'index': ALL}, 'filename'),
)
def filenames_in_component(filenames):
    if (filenames[0] is  None):
        return html.P('Ningún archivo seleccionado.'),
    ficheros = ", ".join(filenames[0]) + "."
    return html.P(children=[ficheros]),
from repositories.algorithm_repository import AlgorithmRepository

#TODO: Guardar en un dcc.Store el configuraiton file en str que luego lo cargaré en btn_result con un json.loads()
@callback(
    [Output('result', 'children'),
    Output('result', 'style'), 
    Output('configuration_file', 'data'),
    Output('uploaded_files', 'data')],
    [Input('algorithm_selected', 'data'),
    Input({'type': 'upload-file', 'index': ALL}, 'filename'),
    Input({'type': 'upload-file', 'index': ALL}, 'contents')]
)
def process_uploaded_files(algorithm_selected, filenames, contents):
    algorithm = algorithm_selected['data']
    if (filenames == []) or (filenames == [None]) or ( algorithm == None):
        return [None, {'visibility': 'hidden'}, None, None]
    try:
        algorithm_repository = AlgorithmRepository()
        uploaded_files_with_format = body_of_uploading_files(filenames[0], contents[0])
        process_files_request = algorithm_repository.process_files(uploaded_files_with_format)
        if process_files_request.status_code != 200:
            error = process_files_request.content.decode('utf-8')
            error_component = html.P(className="error-resultado", children=[f'Se han subido archivos no compatibles, porfavor suba archivos csv o excel. {error}']) 
            return [error_component, {'visibility': 'visible'}, None, None]
        configuration_file_request = algorithm_repository.get_configuration_file(algorithm)
        if configuration_file_request.status_code != 200:
            error = process_files_request.content.decode('utf-8')
            error_component = html.P(className="error-resultado", children=[f'No se ha podido obtener el fichero de configuracion. {error}'])
            return [error_component, {'visibility': 'visible'}, None, None]
        configuration_file_in_text = configuration_file_request.content.decode('utf-8')
        configuration_file = json.loads(configuration_file_in_text)
        n_files = int(configuration_file["n_files"])
        if (len(filenames[0]) is not n_files):
            error_component = html.P(className="error-resultado", children=[f'Este algoritmo requiere {n_files} archivo/s y ha subido {len(filenames[0])} archivo/s.'])
            return [error_component, {'visibility': 'visible'}, None, None]
        btn_result_component = html.Button('Inicio', className="boton-resultado", id={'type': 'boton', 'index': 'btn-resultado'}, n_clicks=0)
        uploaded_files_dataframes = process_files_request.content.decode('utf-8')
        return [btn_result_component, {'visibility': 'visible'}, {'data': configuration_file_in_text}, {'data': uploaded_files_dataframes}]
    except:
        error_component = html.P(className="error-resultado", children=['There is a problem with server conexion.'])
        return [error_component, {'visibility': 'visible'}, None, None]
