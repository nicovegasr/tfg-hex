import json

from dash import ALL, Input, Output, callback, html

from aplication.usecases.check_algorithm import check_algorithm
from aplication.usecases.get_visualizer import get_visualizer
from infrastructure.storage.algorithm_repository import AlgorithmRepository
from infrastructure.http_requesters.algorithm_http_requester import AlgorithmHttpRequester


def create_algorithm_body(algorithm_name: str, algorithm_files: dict):
    body: dict = {}
    body["algorithm_name"] = algorithm_name
    for key, value in algorithm_files.items():
        body[key] = value
    return body


@callback(
    [Output("visualizacion", "children"),
     Output("visualizacion", "style"),
     Output("algorithm_request_body", "data")
    ],
    [
        Input({"type": "boton", "index": ALL}, "n_clicks"),
        Input("algorithm_selected", "data"),
        Input("configuration_file", "data"),
        Input("uploaded_files", "data"),
        Input("uploaded_files_no_processed", "data"),
    ],
)
def show_visualizer_and_download_buttom(
    click,
    algorithm_selected: dict,
    configuration_file_in_storage: dict,
    files_in_storage: dict,
    files_no_processed_in_storage: dict,
):
    if configuration_file_in_storage is None:
        return [None, {"visibility": "hidden"}, None]
    if click[0] == 0:
        return [None, {"visibility": "hidden"}, None]
    try:
        files_in_json = json.loads(files_in_storage["data"])
        configuration_file_in_json = json.loads(configuration_file_in_storage["data"])
        algorithm_name = algorithm_selected["data"]
        check_algorithm(files_in_json, configuration_file_in_json, algorithm_name)

        body = create_algorithm_body(
            algorithm_name, files_no_processed_in_storage["data"]
        )
        algorithm_result_request = AlgorithmHttpRequester.get_algorithm_result(body)
        if algorithm_result_request.status_code != 200:
            raise Exception(
                f"Algo ha ido mal con la ejecución del algoritmo, revisa bien los datos proporcionados: {algorithm_result_request.content.decode('utf-8')}"
            )
        algorithm_result_decode = algorithm_result_request.content.decode("utf-8")
        algorithm_result_decode_in_json = json.loads(algorithm_result_decode)
        visualizer = get_visualizer(
            algorithm_result_decode_in_json, algorithm_name
        )
        AlgorithmRepository.save(algorithm_result_decode_in_json)
        return [visualizer, {"visibility": "visible"}, {"data": body}]
    except Exception as error:
        return [
            html.P(
                style={"color": "red", "background-color": "white"}, children=str(error)
            ),
            {"visibility": "visible"}, None
        ]
