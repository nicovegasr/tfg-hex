import unittest
from unittest.mock import patch

from aplication.usecases.get_available_algorithms import get_available_algorithms


class AvailableAlgorithmsShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_at_least_drivers_algorithm(self) -> None:
        algorithms = get_available_algorithms().index("drivers")
        self.assertEqual(type(algorithms), int)

    @patch("aplication.usecases.get_available_algorithms.os.listdir")
    def test_empty_list_algorithms(self, mock_listdir) -> None:
        mock_listdir.return_value = []
        self.assertListEqual(get_available_algorithms(), [])

    @patch("aplication.usecases.get_available_algorithms.os.listdir")
    def test_no_algorithm_in(self, mock_listdir) -> None:
        mock_listdir.side_effect = ValueError(
            "Something is wrong with algorithm path files"
        )
        with self.assertRaises(ValueError):
            get_available_algorithms()
