from aplication.usecases.process_algorithm_files import process_algorithm_files
from domain.algorithms.algorithm import Algorithm


def get_algorithm_result(files: dict):
    try:
        algorithm_name = files.pop("algorithm_name", None)
        if not algorithm_name:
            raise Exception("Algorithm name not specified.")
        if not files:
            raise Exception("Algorithm files not specified.")
        files_in_dataframe = process_algorithm_files(files)
        algorithm = Algorithm(algorithm_name)
        return algorithm.start(files_in_dataframe)
    except Exception as Error:
        raise Exception(str(Error))
