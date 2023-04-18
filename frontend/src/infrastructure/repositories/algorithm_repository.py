import requests


class AlgorithmRepository:
    def __init__(self):
        self.api_url = "http://127.0.0.1:3000/"
        pass

    def get_available_algorithms(self) -> requests:
        algorithm_availables = requests.get(
            f"{self.api_url + 'available_algorithms'}")
        return algorithm_availables

    def get_algorithm_description(self, algorithm: str) -> requests:
        algorithm_availables = requests.get(
            f"{self.api_url + 'description' + '?algorithm_name=' + algorithm }")
        return algorithm_availables
    
    def process_files(self, files: dict) -> requests:
        response = requests.post('/process_files', json=files)
        pass
