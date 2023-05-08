import unittest

from aplication.usecases.get_configuration_file import get_configuration_file


class ConfigurationFileShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_at_least_drivers_configuration(self) -> None:
        algorithms = get_configuration_file("drivers")
        self.assertEqual(type(algorithms), dict)

    def test_get_no_configuration_file(self) -> None:
        self.assertRaises(ValueError, get_configuration_file, "Non-existent")
