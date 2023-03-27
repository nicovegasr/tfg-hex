import unittest
from unittest.mock import patch
import config_modules
config_modules.add()
from infrastructure.api.server import app

class AvailableAlgorithmShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_available_algorithms_from_client(self) -> None:
        with app.test_client() as client:
            response = client.get('/available_algorithms')
            assert response.status_code == 200

    def test_not_found_available_algorithms_from_client(self):
        with app.test_client() as client:
            with patch('src.aplication.usecases.get_available_algorithms.get_available_algorithms', return_value=[]):
                response = client.get('/available_algorithms')
                assert response.status_code == 404

if __name__ == '__main__':
    unittest.main()