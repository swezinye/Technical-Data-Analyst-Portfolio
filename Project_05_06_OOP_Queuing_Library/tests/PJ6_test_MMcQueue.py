# Project6/PJ6_test_MMcQueue.py
import math
import unittest

from MMcQueue import MMcQueue


def erlang_c_expected(lam, mu, c):
    """Compute expected (P0, Lq, Wq, W, L) using Erlang-C theory."""
    a = lam / mu
    rho = a / c
    if lam <= 0 or mu <= 0 or c < 1 or rho >= 1:
        return (math.inf, math.inf, math.inf, math.inf, math.inf)

    series = sum((a ** n) / math.factorial(n) for n in range(c))
    tail = (a ** c) / (math.factorial(c) * (1.0 - rho))
    p0 = 1.0 / (series + tail)

    p_wait = tail * p0
    lq = p_wait * (rho / (1.0 - rho))
    wq = lq / lam
    w = wq + 1.0 / mu
    l = lam * w
    return (p0, lq, wq, w, l)


class TestMMcQueue(unittest.TestCase):
    def test_validity_and_feasibility(self):
        q1 = MMcQueue(20, 25, 1)
        q2 = MMcQueue(24, 25, 2)
        self.assertTrue(q1.is_valid()); self.assertTrue(q1.is_feasible())
        self.assertTrue(q2.is_valid()); self.assertTrue(q2.is_feasible())

        bad = MMcQueue(20, 25, 0)
        self.assertFalse(bad.is_valid())

    def test_erlang_c_numbers_for_c2(self):
        # λ=24, μ=25, c=2
        q = MMcQueue(24, 25, 2)
        p0_e, lq_e, wq_e, w_e, l_e = erlang_c_expected(24, 25, 2)

        self.assertAlmostEqual(q.p0, p0_e, places=7)
        self.assertAlmostEqual(q.lq, lq_e, places=7)
        self.assertAlmostEqual(q.wq, wq_e, places=7)
        self.assertAlmostEqual(q.w,  w_e,  places=7)
        self.assertAlmostEqual(q.l,  l_e,  places=7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
