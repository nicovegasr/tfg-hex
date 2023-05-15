import unittest

from aplication.usecases.get_algorithm_description import get_algorithm_description
from aplication.usecases.get_configuration_file import get_configuration_file

class DescriptionAlgorithmShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_driver_description(self) -> None:
        configuration_file = get_configuration_file("drivers")
        description = get_algorithm_description(configuration_file)
        self.assertEqual(len(description), 2)

    def test_get_not_existent_algorithm_description(self) -> None:
        self.assertRaises(ValueError, get_algorithm_description, "Non-existent")
