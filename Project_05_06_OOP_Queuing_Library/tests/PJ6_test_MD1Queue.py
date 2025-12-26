import math
import unittest

from MMcPriorityQueue import MMcPriorityQueue

class TestMMcPriorityQueue(unittest.TestCase):
    def setUp(self):
        # canonical case from lecture sheet
        self.q = MMcPriorityQueue((5, 10, 5), 25, 1)
        self.q._calc_metrics()   # trigger lazy compute once for deterministic tests

    def test_getters_and_validity(self):
        self.assertTrue(self.q.is_valid())
        # aggregated λ should be 20 if your class exposes lamda
        if hasattr(self.q, "lamda"):
            self.assertAlmostEqual(self.q.lamda, 20.0)
        # individual λk getters
        self.assertAlmostEqual(self.q.get_lamda_k(1), 5.0)
        self.assertAlmostEqual(self.q.get_lamda_k(2), 10.0)
        self.assertAlmostEqual(self.q.get_lamda_k(3), 5.0)

    def test_aggregate_metrics_match_mm1_for_c1(self):
        # With c=1 and total λ=20, μ=25, the aggregate behaves like M/M/1
        self.assertAlmostEqual(self.q.p0, 0.2, places=7)
        self.assertAlmostEqual(self.q.lq, 3.2, places=7)
        self.assertAlmostEqual(self.q.l, 4.0, places=7)
        self.assertAlmostEqual(self.q.wq, 0.16, places=7)
        self.assertAlmostEqual(self.q.w, 0.20, places=7)

    def test_per_class_waits_and_lengths(self):
        # Expected values from lecture rubric for (5,10,5), μ=25, c=1
        exp_wqk = (0.04, 0.10, 0.40)
        exp_wk  = (0.08, 0.14, 0.44)
        exp_lqk = (0.2, 1.0, 2.0)
        exp_lk  = (0.4, 1.4, 2.2)
        exp_bk  = (0.8, 0.4, 0.2)

        for k, v in enumerate(exp_wqk, 1):
            self.assertAlmostEqual(self.q.get_wq_k(k), v, places=7)
        for k, v in enumerate(exp_wk, 1):
            self.assertAlmostEqual(self.q.get_w_k(k), v, places=7)
        for k, v in enumerate(exp_lqk, 1):
            self.assertAlmostEqual(self.q.get_lq_k(k), v, places=7)
        for k, v in enumerate(exp_lk, 1):
            self.assertAlmostEqual(self.q.get_l_k(k), v, places=7)
        for k, v in enumerate(exp_bk, 1):
            self.assertAlmostEqual(self.q.get_b_k(k), v, places=7)

    def test_invalid_tuple_is_caught(self):
        bad = MMcPriorityQueue((5, 10, "five"), 25, 1)
        self.assertFalse(bad.is_valid())
        # Accessors should surface NaN for invalid state
        self.assertTrue(math.isnan(bad.get_wq_k(1)))
        self.assertTrue(math.isnan(bad.p0))

if __name__ == "__main__":
    unittest.main(verbosity=2)
