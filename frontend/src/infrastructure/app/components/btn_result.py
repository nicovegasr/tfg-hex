import json
import pandas as pd
from flask import Response
from dash import html, callback, Input, Output, State, ALL, ctx
from aplication.usecases.check_algorithm import check_algorithm
from aplication.usecases.check_algorithm import check_algorithm
from aplication.usecases.get_visualizer import get_visualizer
from infrastructure.http_requesters.algorithm_http_requester import AlgorithmHttpRequester

def create_algorithm_body(algorithm_name: str, algorithm_files: dict):
    body: dict = {}
    body['algorithm_name'] = algorithm_name
    for key, value in algorithm_files.items():
        body[key] = value
    return body    

@callback(
    [Output('visualizacion', 'children'),
     Output('visualizacion', 'style')],
    [Input({'type': 'boton', 'index': ALL}, 'n_clicks'),
     Input('algorithm_selected', 'data'),
     Input('configuration_file', 'data'),
     Input('uploaded_files', 'data'),
     Input('uploaded_files_no_processed', 'data')]
    )
def show_visualizer_and_download_buttom(click, algorithm_selected: dict, configuration_file_in_storage: dict, files_in_storage: dict, files_no_processed_in_storage: dict):
    if configuration_file_in_storage is None:
        return [None, {'visibility' : 'hidden'}]
    if (click[0] == 0):
        return [None, {'visibility' : 'hidden'}]
    try:
        files_in_json = json.loads(files_in_storage["data"])
        configuration_file_in_json = json.loads(configuration_file_in_storage["data"])
        algorithm_name = algorithm_selected['data']
        check_algorithm(files_in_json, configuration_file_in_json, algorithm_name)        
        body = create_algorithm_body(algorithm_name, files_no_processed_in_storage["data"])
        algorithm_result_request = AlgorithmHttpRequester.get_algorithm_result(body)
        if (algorithm_result_request.status_code != 200): 
            raise Exception(f"Algo ha ido mal con la ejecución del algoritmo, revisa bien los datos proporcionados: {algorithm_result_request.content.decode('utf-8')}")
        visualizer = get_visualizer(algorithm_result_request.content.decode('utf-8'), algorithm_name)
        return [visualizer, {'visibility' : 'visible'}]
    except Exception as error:
        return [html.P(style={'color' : 'red', 'background-color' : 'white'}, children=str(error)), {'visibility' : 'visible'}]