import unittest

import config_modules
config_modules.add()
from infrastructure.api.server import app

class DescriptionAlgorithmShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_driver_description(self) -> None:
        with app.test_client() as client:
            response = client.get('/description?algorithm_name=drivers')
            assert response.status_code == 200

    def test_get_not_existent_algorithm_description(self) -> None:
        with app.test_client() as client:
            response = client.get('/description?algorithm_name=non-existent')
            assert response.status_code == 404

if __name__ == '__main__':
    unittest.main()