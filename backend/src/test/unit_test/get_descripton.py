import unittest

import config_modules
config_modules.add()

from aplication.usecases.get_algorithm_description import get_algorithm_description

class DescriptionAlgorithmShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_driver_description(self) -> None:
        description = get_algorithm_description("drivers")
        self.assertEquals(len(description), 2)

    def test_get_not_existent_algorithm_description(self) -> None:
        description = get_algorithm_description("drivers")
        self.assertEquals(len(description), 0)


if __name__ == '__main__':

    unittest.main()
