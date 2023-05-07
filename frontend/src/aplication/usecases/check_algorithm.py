import importlib
from src.domain.entitities.check.default import DefaultCheck
from .split_files import split_files_and_filenames

def check_algorithm(files: dict, configuration_file: dict, algorithm_name: str) -> None:
    filenames, files_contents = split_files_and_filenames(files)
    checker = DefaultCheck(filenames, files_contents, configuration_file)
    checker.start()
    if importlib.util.find_spec(f"src.domain.entitities.check.{algorithm_name}"):
        algorithm_checker = importlib.import_module(f"src.domain.entitities.check.{algorithm_name}")
        algorithm_checker.start(filenames, files_contents, configuration_file)
