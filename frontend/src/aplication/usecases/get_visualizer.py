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


def get_visualizer(files_in_json: list[dict], algorithm_name: str):
    files_in_dataframe = []
    for file in files_in_json:
        files_in_dataframe.append(pd.read_json(file))
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
