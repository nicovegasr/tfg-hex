import requests

class AlgorithmHttpRequester:
    api_url = "http://127.0.0.1:3000/"

    @staticmethod
    def get_available_algorithms() -> requests:
        response = requests.get(
            f"{AlgorithmHttpRequester.api_url}available_algorithms")
        return response
    
    @staticmethod
    def get_algorithm_description( algorithm: str) -> requests:
        response = requests.get(
            f"{AlgorithmHttpRequester.api_url + 'description' + '?algorithm_name=' + algorithm }")
        return response
    
    @staticmethod
    def process_files( files: dict) -> requests:
        response = requests.post(f"{AlgorithmHttpRequester.api_url}process_files", json=files)
        return response
    
    @staticmethod
    def get_configuration_file(algorithm: str) -> requests:
        response = requests.get(f"{AlgorithmHttpRequester.api_url}configuration_file?algorithm_name={algorithm}")
        return response
    
    @staticmethod
    def get_algorithm_result(body: dict) -> requests:
        response = requests.post(f"{AlgorithmHttpRequester.api_url}algorithm_performance", json=body)
        return response