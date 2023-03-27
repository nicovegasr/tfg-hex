import unittest
from unittest.mock import patch
import config_modules
config_modules.add()
from infrastructure.api.server import app

class AvailableAlgorithmsShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_at_least_drivers_algorithm(self) -> None:
        with app.test_client() as client:
            response = client.get('/available_algorithms')
            assert response.status_code == 200

    def test_available_algorithms_not_found(self):
        with app.test_client() as client:
            with patch('src.aplication.usecases.get_available_algorithms.get_available_algorithms', return_value=[]):
                response = client.get('/available_algorithms')
                assert response.status_code == 404

if __name__ == '__main__':
    unittest.main()