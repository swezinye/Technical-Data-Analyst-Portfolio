import math
import unittest

from MM1Queue import MM1Queue

class TestMM1Queue(unittest.TestCase):
    def test_valid_and_feasible(self):
        good = MM1Queue(20, 25)
        bad  = MM1Queue("twenty", 25)
        inf  = MM1Queue(25, 20)

        self.assertTrue(good.is_valid())
        self.assertTrue(good.is_feasible())

        self.assertFalse(bad.is_valid())
        self.assertFalse(inf.is_feasible())

    def test_mm1_theory_numbers(self):
        # ρ = 0.8
        q = MM1Queue(20, 25)
        self.assertAlmostEqual(q.p0, 0.2)
        self.assertAlmostEqual(q.lq, 3.2, places=7)
        self.assertAlmostEqual(q.l, 4.0, places=7)
        self.assertAlmostEqual(q.wq, 0.16, places=7)
        self.assertAlmostEqual(q.w, 0.20, places=7)

    def test_invalid_propagation(self):
        q = MM1Queue(20, 0)
        self.assertFalse(q.is_valid())
        self.assertTrue(math.isnan(q.p0))
        self.assertTrue(math.isnan(q.lq))

if __name__ == "__main__":
    unittest.main(verbosity=2)
