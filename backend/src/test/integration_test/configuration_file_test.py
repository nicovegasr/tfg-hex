import unittest
from unittest.mock import patch
import config_modules
config_modules.add()
from infrastructure.api.server import app

class ConfigurationFileShould(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_driver_configuration_file(self) -> None:
        with app.test_client() as client:
            response = client.get('/configuration_file?algorithm_name=drivers')
            assert response.status_code == 200

    def test_try_get_non_existent_configuration_file(self) -> None:
        with app.test_client() as client:
            response = client.get('/configuration_file?algorithm_name=non-existent')
            assert response.status_code == 404

if __name__ == '__main__':
    unittest.main()