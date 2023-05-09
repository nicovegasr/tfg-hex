import importlib
import json

import pandas as pd
from dash import html

from domain.entitities.visualizer.default import visualizer


def add_download_button():
    return html.Button(
        "Descargar",
        id={"type": "btn-descarga", "index": "btn-descarga"},
        className="boton-descarga",
        n_clicks=0,
    )


def get_visualizer(files, algorithm_name):
    files_in_json: list = json.loads(files)
    files_in_dataframe = []
    for file in files_in_json:
        files_in_dataframe.append(pd.DataFrame.from_dict(file))
    if importlib.util.find_spec(f"src.domain.entitities.visualizer.{algorithm_name}"):
        algorithm_visualizer_module = importlib.import_module(
            f"src.domain.entitities.visualizer.{algorithm_name}"
        )
        algorithm_visualizer = algorithm_visualizer_module.visualizer(
            files_in_dataframe
        )
    else:
        algorithm_visualizer = visualizer(files_in_dataframe)
    algorithm_visualizer.append(add_download_button())
    return algorithm_visualizer
