from process_algorithm_files import process_algorithm_files
from domain.algorithms.algorithm import Algorithm
def get_algorithm_result(files: dict):
    try:
        algorithm_name = files.pop("algorithm_name")
        files_in_dataframe = process_algorithm_files(files)
        algorithm = Algorithm(algorithm_name)
        return algorithm.start(files_in_dataframe)
    except Exception as Error:
        return str(Error)
