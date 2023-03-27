import unittest

import config_modules
config_modules.add()
from aplication.usecases.get_algorithm_result import get_algorithm_result

class AlgorithmDriverResultShould(unittest.TestCase):
    def setup(self):
        pass

    def test_get_driver_result(self) -> None:
        pass

if __name__ == '__main__':
    unittest.main()