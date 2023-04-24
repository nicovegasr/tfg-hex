import json
from dash import html, callback, Input, Output, State, ALL, ctx
from aplication.usecases.check_algorithm import check_algorithm

#TODO: HAcer el callback con varios output y pasarle tanto algorithm selected como el configuration file por Iput del dcc.Store y los files subidos que a lo mejor seria buena idea pasar directamente desde un dcc.Store el formato del body que ya tengo.
# Al hacer click llamaremos a Comprobar, al Algoritmo y a Visualizacion.
@callback(
    [Output('visualizacion', 'children'),
     Output('visualizacion', 'style')],
    [Input({'type': 'boton', 'index': ALL}, 'n_clicks'),
     Input('algorithm_selected', 'data'),
     Input('configuration_file', 'data'),
     Input('uploaded_files', 'data')]
    )
def show_visualizer_and_download_buttom(click, algorithm, configuration_file_in_sotorage, files_in_storage):
    if configuration_file_in_sotorage is None:
        return [None, {'visibility': 'hidden'}]
    if (click[0] == 0):
        return [None, {'visibility': 'hidden'}]
    files_in_dataframe = json.loads(files_in_storage["data"])
    configuration_file_in_dataframe = json.loads(configuration_file_in_sotorage["data"])
    check_algorithm(files_in_dataframe, configuration_file_in_dataframe)
    return [None, {'visibility': 'hidden'}]