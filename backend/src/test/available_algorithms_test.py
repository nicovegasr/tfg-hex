import unittest

import config_modules
config_modules.add()
from aplication.usecases.get_available_algorithms import get_available_algorithms

class AvailableAlgorithmsShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_at_least_drivers_algorithm(self) -> None:
        algorithms = get_available_algorithms().index("drivers")
        self.assertEqual(type(algorithms), int)

    def test_no_algorithm_in(self) -> None:
        self.assertRaises(ValueError, get_available_algorithms().index, "Non-existent")


if __name__ == '__main__':
    unittest.main()