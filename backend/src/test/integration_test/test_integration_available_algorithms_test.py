import unittest
from unittest.mock import patch

from infrastructure.api.server import app


class AvailableAlgorithmShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_available_algorithms_from_client(self) -> None:
        with app.test_client() as client:
            response = client.get("/available_algorithms")
            assert response.status_code == 200

    def test_not_found_available_algorithms_from_client(self):
        with app.test_client() as client:
            with patch(
                "aplication.usecases.get_available_algorithms.get_available_algorithms",
                return_value=[],
            ):
                response = client.get("/available_algorithms")
                assert response.status_code == 404

    def test_path_error_in_server(self):
        with app.test_client() as client:
            with patch(
                "aplication.usecases.get_available_algorithms.get_available_algorithms",
                side_effect=ValueError("Something is wrong with algorithm path files"),
            ):
                response = client.get("/available_algorithms")
                assert response.status_code == 501


if __name__ == "__main__":
    unittest.main()
