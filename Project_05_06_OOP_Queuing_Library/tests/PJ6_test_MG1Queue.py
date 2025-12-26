import math
import unittest
from MG1Queue import MG1Queue

class TestMG1Queue(unittest.TestCase):
    def setUp(self):
        # basic valid instance
        self.q = MG1Queue(20, 25, 5)

    def test_valid(self):
        self.assertTrue(self.q.is_valid())
        invalid = MG1Queue(20, 0, -5)
        self.assertFalse(invalid.is_valid())

    def test_feasible(self):
        self.assertTrue(self.q.is_feasible())
        infeasible = MG1Queue(25, 20, 5)
        self.assertFalse(infeasible.is_feasible())

    def test_metrics(self):
        self.q._calc_metrics()
        self.assertAlmostEqual(self.q.p0, 1 - (20 / 25))
        expected_lq = ((20/25)**2 + (20**2 * 5**2)) / (2*(1 - (20/25)))
        self.assertAlmostEqual(self.q.lq, expected_lq)

if __name__ == "__main__":
    unittest.main()
