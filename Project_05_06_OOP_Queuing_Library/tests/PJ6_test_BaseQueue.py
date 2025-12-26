import math
import unittest

from BaseQueue import BaseQueue

class DummyQueue(BaseQueue):
    """Tiny concrete child so we can exercise BaseQueue laziness/derived props.
       Implements M/M/1 formulas (for testing only)."""
    def _calc_metrics(self):
        if not self.is_valid():
            self._p0 = math.nan
            self._lq = math.nan
        elif not self.is_feasible():
            self._p0 = math.inf
            self._lq = math.inf
        else:
            rho = self.ro
            self._p0 = 1.0 - rho
            self._lq = (rho * rho) / (1.0 - rho)
        self._recalc_needed = False

class TestBaseQueue(unittest.TestCase):
    def test_getters_setters_and_laziness(self):
        q = DummyQueue(20, 25)               # valid, feasible
        _ = q.lq                              # trigger calc
        self.assertFalse(q._recalc_needed)

        q.lamda = 22                          # use property, not private attr
        self.assertTrue(q._recalc_needed)     # laziness: marked dirty

        # invalid mu
        q.mu = 0
        self.assertFalse(q.is_valid())
        self.assertTrue(math.isnan(q.l))

    def test_utilization_and_waits(self):
        q = DummyQueue(20, 25)
        self.assertAlmostEqual(q.ro, 0.8)
        # M/M/1 expectations
        self.assertAlmostEqual(q.p0, 0.2)
        self.assertAlmostEqual(q.lq, 3.2, places=7)
        self.assertAlmostEqual(q.l, 4.0, places=7)
        self.assertAlmostEqual(q.wq, 0.16, places=7)
        self.assertAlmostEqual(q.w, 0.20, places=7)

if __name__ == "__main__":
    unittest.main(verbosity=2)
