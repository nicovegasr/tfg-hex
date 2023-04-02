import importlib

class Algorithm:
    def __init__(self, name) -> None:
        self.algorithm_name = name

    def start(self, files):
      algorithm_result = importlib.import_module(f"files.{self.algorithm_name}.algorithm")
      result = algorithm_result.algorithm(files)
      return result