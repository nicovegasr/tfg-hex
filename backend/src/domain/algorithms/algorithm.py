import datetime
import importlib
import json

import pandas as pd


class Algorithm:
    def __init__(self, name) -> None:
        self.algorithm_name = name

    def start(self, files):
        algorithm_result = importlib.import_module(
            f"domain.algorithms.files.{self.algorithm_name}.algorithm"
        )
        result = algorithm_result.algorithm(files)
        formated_result = self.formating_result(result)
        return formated_result

    def formating_result(self, files: dict):
        filenames, file_contents = self.split_files_and_filenames(files)
        formated_result: list[dict] = []
        for file_index in range(len(file_contents)):
            file_in_dataframe: pd.DataFrame = file_contents[file_index]
            file_in_dataframe["Fichero_Origen"] = filenames[file_index]
            file_in_dataframe["Hora_ejecucion"] = datetime.datetime.now().strftime(
                "%m/%d/%Y-%H:%M:%S"
            )
            file_in_json = file_in_dataframe.to_dict()
            formated_result.append(file_in_json)
        return formated_result

    def split_files_and_filenames(self, files: dict):
        filenames = []
        file_contents = []
        for file_key in files:
            file = files[file_key]
            filenames.append(file["filename"])
            file_contents.append(
                pd.DataFrame.from_dict(json.loads(file["file_content"]))
            )
        return filenames, file_contents
