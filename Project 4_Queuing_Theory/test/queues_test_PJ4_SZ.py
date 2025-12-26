import unittest
import math
import queues as q


class TestQueuesStudent(unittest.TestCase):
    """Test suite for queueing theory functions"""

    def setUp(self):
        """Set up common test values"""
        self.lamda = 20.0
        self.mu = 25.0
        self.c = 1

    # ==================== Tests for is_valid ====================
    def test_is_valid_basic(self):
        """Test is_valid with basic valid inputs"""
        self.assertTrue(q.is_valid(20, 25, 1))
        self.assertTrue(q.is_valid(15, 30, 2))
        self.assertTrue(q.is_valid(10, 20, 3))

    def test_is_valid_tuple_lamda(self):
        """Test is_valid with tuple arrival rates"""
        self.assertTrue(q.is_valid((5, 10, 5), 25, 1))
        self.assertTrue(q.is_valid((10, 20), 30, 2))
        self.assertTrue(q.is_valid((15,), 25, 1))

    def test_is_valid_invalid_lamda(self):
        """Test is_valid rejects invalid lambda values"""
        self.assertFalse(q.is_valid(0, 25, 1))
        self.assertFalse(q.is_valid(-20, 25, 1))
        self.assertFalse(q.is_valid((5, -10, 5), 25, 1))
        self.assertFalse(q.is_valid("twenty", 25, 1))

    def test_is_valid_invalid_mu(self):
        """Test is_valid rejects invalid mu values"""
        self.assertFalse(q.is_valid(20, 0, 1))
        self.assertFalse(q.is_valid(20, -25, 1))
        self.assertFalse(q.is_valid(20, "twenty-five", 1))

    def test_is_valid_invalid_c(self):
        """Test is_valid rejects invalid c values"""
        self.assertFalse(q.is_valid(20, 25, 0))
        self.assertFalse(q.is_valid(20, 25, -1))
        self.assertFalse(q.is_valid(20, 25, "one"))

    # ==================== Tests for is_feasible ====================
    def test_is_feasible_valid_systems(self):
        """Test is_feasible with valid feasible systems"""
        self.assertTrue(q.is_feasible(20, 25, 1))  # ρ = 0.8
        self.assertTrue(q.is_feasible(40, 25, 2))  # ρ = 0.8
        self.assertTrue(q.is_feasible(50, 25, 3))  # ρ = 0.667

    def test_is_feasible_infeasible_systems(self):
        """Test is_feasible with infeasible systems (ρ >= 1)"""
        self.assertFalse(q.is_feasible(25, 25, 1))  # ρ = 1.0
        self.assertFalse(q.is_feasible(30, 25, 1))  # ρ > 1.0
        self.assertFalse(q.is_feasible(50, 25, 2))  # ρ = 1.0

    def test_is_feasible_tuple_lamda(self):
        """Test is_feasible with tuple arrival rates"""
        self.assertTrue(q.is_feasible((5, 10, 5), 25, 1))  # Total = 20
        self.assertFalse(q.is_feasible((10, 10, 10), 25, 1))  # Total = 30

    def test_is_feasible_invalid_inputs(self):
        """Test is_feasible returns False for invalid inputs"""
        self.assertFalse(q.is_feasible(0, 25, 1))
        self.assertFalse(q.is_feasible(20, 0, 1))
        self.assertFalse(q.is_feasible(-20, 25, 1))

    # ==================== Tests for calc_p0 ====================
    def test_calc_p0_mm1(self):
        """Test calc_p0 for M/M/1 queues"""
        self.assertAlmostEqual(0.2, q.calc_p0(20, 25, 1), places=5)
        self.assertAlmostEqual(0.4, q.calc_p0(15, 25, 1), places=5)

    def test_calc_p0_mmc(self):
        """Test calc_p0 for M/M/c queues"""
        self.assertAlmostEqual(0.0345423, q.calc_p0(65, 25, 3), places=5)
        # Add more M/M/c tests as needed

    def test_calc_p0_invalid(self):
        """Test calc_p0 returns nan for invalid inputs"""
        self.assertTrue(math.isnan(q.calc_p0(0, 25, 1)))
        self.assertTrue(math.isnan(q.calc_p0(20, 0, 1)))
        self.assertTrue(math.isnan(q.calc_p0(-20, 25, 1)))

    def test_calc_p0_infeasible(self):
        """Test calc_p0 returns inf for infeasible systems"""
        self.assertTrue(math.isinf(q.calc_p0(25, 25, 1)))
        self.assertTrue(math.isinf(q.calc_p0(30, 25, 1)))

    # ==================== Tests for calc_lq_mmc ====================
    def test_calc_lq_mmc_mm1(self):
        """Test calc_lq_mmc for M/M/1 queues"""
        self.assertAlmostEqual(3.2, q.calc_lq_mmc(20, 25, 1), places=4)

    def test_calc_lq_mmc_mmc(self):
        """Test calc_lq_mmc for M/M/c queues"""
        self.assertAlmostEqual(2.8444, q.calc_lq_mmc(40, 25, 2), places=4)
        self.assertAlmostEqual(0.8889, q.calc_lq_mmc(50, 25, 3), places=4)

    def test_calc_lq_mmc_tuple_lamda(self):
        """Test calc_lq_mmc with tuple arrival rates"""
        self.assertAlmostEqual(3.2, q.calc_lq_mmc((5, 10, 5), 25, 1), places=4)
        self.assertAlmostEqual(2.8444, q.calc_lq_mmc((10, 15, 15), 25, 2), places=4)

    def test_calc_lq_mmc_invalid(self):
        """Test calc_lq_mmc returns nan for invalid inputs"""
        self.assertTrue(math.isnan(q.calc_lq_mmc(0, 25, 1)))
        self.assertTrue(math.isnan(q.calc_lq_mmc(20, 0, 1)))

    def test_calc_lq_mmc_infeasible(self):
        """Test calc_lq_mmc returns inf for infeasible systems"""
        self.assertTrue(math.isinf(q.calc_lq_mmc(25, 25, 1)))
        self.assertTrue(math.isinf(q.calc_lq_mmc(30, 25, 1)))

    # ==================== Tests for calc_bk_mmc ====================
    def test_calc_bk_mmc_basic(self):
        """Test calc_bk_mmc with priority queue"""
        self.assertAlmostEqual(1.0, q.calc_bk_mmc(0, (5, 10, 5), 25, 1), places=5)
        self.assertAlmostEqual(0.8, q.calc_bk_mmc(1, (5, 10, 5), 25, 1), places=5)
        self.assertAlmostEqual(0.4, q.calc_bk_mmc(2, (5, 10, 5), 25, 1), places=5)

    def test_calc_bk_mmc_single_lamda(self):
        """Test calc_bk_mmc with single arrival rate"""
        self.assertAlmostEqual(1.0, q.calc_bk_mmc(0, 20, 25, 1), places=5)
        self.assertAlmostEqual(0.2, q.calc_bk_mmc(1, 20, 25, 1), places=5)
        # k > 1 should return nan for single lamda
        self.assertTrue(math.isnan(q.calc_bk_mmc(2, 20, 25, 1)))

    def test_calc_bk_mmc_invalid(self):
        """Test calc_bk_mmc returns nan for invalid inputs"""
        self.assertTrue(math.isnan(q.calc_bk_mmc(-1, 20, 25, 1)))
        self.assertTrue(math.isnan(q.calc_bk_mmc(1, -20, 25, 1)))
        self.assertTrue(math.isnan(q.calc_bk_mmc(1, 20, -25, 1)))

    def test_calc_bk_mmc_infeasible(self):
        """Test calc_bk_mmc returns inf for infeasible systems"""
        self.assertTrue(math.isinf(q.calc_bk_mmc(1, 30, 25, 1)))

    # ==================== Tests for calc_wqk_mmc ====================
    def test_calc_wqk_mmc_priority(self):
        """Test calc_wqk_mmc with priority classes"""
        self.assertAlmostEqual(0.04, q.calc_wqk_mmc(1, (5, 10, 5), 25, 1), places=5)
        self.assertAlmostEqual(0.1, q.calc_wqk_mmc(2, (5, 10, 5), 25, 1), places=5)
        self.assertAlmostEqual(0.4, q.calc_wqk_mmc(3, (5, 10, 5), 25, 1), places=5)

    def test_calc_wqk_mmc_single_tuple(self):
        """Test calc_wqk_mmc with single-element tuple"""
        self.assertAlmostEqual(0.16, q.calc_wqk_mmc(1, (20,), 25, 1), places=5)
        self.assertTrue(math.isnan(q.calc_wqk_mmc(2, (20,), 25, 1)))

    def test_calc_wqk_mmc_scalar(self):
        """Test calc_wqk_mmc with scalar lamda"""
        self.assertAlmostEqual(0.16, q.calc_wqk_mmc(1, 20, 25, 1), places=5)
        self.assertTrue(math.isnan(q.calc_wqk_mmc(2, 20, 25, 1)))

    def test_calc_wqk_mmc_invalid(self):
        """Test calc_wqk_mmc returns nan for invalid inputs"""
        self.assertTrue(math.isnan(q.calc_wqk_mmc(0, (5, 10), 25, 1)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(-1, (5, 10), 25, 1)))
        self.assertTrue(math.isnan(q.calc_wqk_mmc(3, (5, 10), 25, 1)))  # k > len

    def test_calc_wqk_mmc_infeasible(self):
        """Test calc_wqk_mmc returns inf for infeasible systems"""
        self.assertTrue(math.isinf(q.calc_wqk_mmc(1, (20, 20), 25, 1)))

    # ==================== Tests for calc_lqk_mmc ====================
    def test_calc_lqk_mmc_basic(self):
        """Test calc_lqk_mmc with valid inputs"""
        lamda = (10, 15, 20)
        wqk = 0.5
        # lqk = lamda[k-1] * wqk
        self.assertAlmostEqual(5.0, q.calc_lqk_mmc(1, lamda, wqk), places=5)
        self.assertAlmostEqual(7.5, q.calc_lqk_mmc(2, lamda, wqk), places=5)
        self.assertAlmostEqual(10.0, q.calc_lqk_mmc(3, lamda, wqk), places=5)

    def test_calc_lqk_mmc_invalid_k(self):
        """Test calc_lqk_mmc returns nan for invalid k"""
        lamda = (10, 15, 20)
        wqk = 0.5
        self.assertTrue(math.isnan(q.calc_lqk_mmc(0, lamda, wqk)))
        self.assertTrue(math.isnan(q.calc_lqk_mmc(-1, lamda, wqk)))
        self.assertTrue(math.isnan(q.calc_lqk_mmc(4, lamda, wqk)))

    def test_calc_lqk_mmc_invalid_inputs(self):
        """Test calc_lqk_mmc returns nan for invalid inputs"""
        self.assertTrue(math.isnan(q.calc_lqk_mmc(1, "invalid", 0.5)))
        self.assertTrue(math.isnan(q.calc_lqk_mmc(1, (10, 15), "invalid")))
        self.assertTrue(math.isnan(q.calc_lqk_mmc(1, (10, 15), -0.5)))

    # ==================== Tests for use_littles_law ====================
    def test_use_littles_law_from_lq(self):
        """Test use_littles_law calculating from Lq"""
        result = q.use_littles_law(20, 25, 1, lq=3.2)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(3.2, result['lq'], places=5)
        self.assertAlmostEqual(4.0, result['l'], places=5)
        self.assertAlmostEqual(0.16, result['wq'], places=5)
        self.assertAlmostEqual(0.2, result['w'], places=5)
        self.assertAlmostEqual(0.8, result['r'], places=5)
        self.assertAlmostEqual(0.8, result['ro'], places=5)

    def test_use_littles_law_from_l(self):
        """Test use_littles_law calculating from L"""
        result = q.use_littles_law(20, 25, 1, l=4.0)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(3.2, result['lq'], places=5)
        self.assertAlmostEqual(4.0, result['l'], places=5)

    def test_use_littles_law_from_wq(self):
        """Test use_littles_law calculating from Wq"""
        result = q.use_littles_law(20, 25, 1, wq=0.16)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(0.16, result['wq'], places=5)
        self.assertAlmostEqual(3.2, result['lq'], places=5)

    def test_use_littles_law_from_w(self):
        """Test use_littles_law calculating from W"""
        result = q.use_littles_law(20, 25, 1, w=0.2)
        self.assertIsNotNone(result)
        self.assertAlmostEqual(0.2, result['w'], places=5)
        self.assertAlmostEqual(4.0, result['l'], places=5)

    def test_use_littles_law_priority_queue(self):
        """Test use_littles_law with priority queue (multiple classes)"""
        result = q.use_littles_law((5, 20, 30), 25, 3, lq=1.49094)
        self.assertIsNotNone(result)
        # Should have wqk and lqk for multiple classes
        self.assertIn('wqk', result)
        self.assertIn('lqk', result)
        self.assertEqual(3, len(result['wqk']))
        self.assertEqual(3, len(result['lqk']))

    def test_use_littles_law_single_tuple_no_priority(self):
        """Test use_littles_law with single-element tuple (no priority metrics)"""
        result = q.use_littles_law((55,), 25, 3, lq=1.49094)
        self.assertIsNotNone(result)
        # Should NOT have wqk and lqk for single class
        self.assertNotIn('wqk', result)
        self.assertNotIn('lqk', result)

    def test_use_littles_law_no_kwargs(self):
        """Test use_littles_law returns None when no metric provided"""
        result = q.use_littles_law(20, 25, 1)
        self.assertIsNone(result)

    def test_use_littles_law_invalid_inputs(self):
        """Test use_littles_law returns nan for invalid inputs"""
        self.assertTrue(math.isnan(q.use_littles_law(0, 25, 1, lq=3.2)))
        self.assertTrue(math.isnan(q.use_littles_law(20, 0, 1, lq=3.2)))

    def test_use_littles_law_infeasible(self):
        """Test use_littles_law returns inf for infeasible systems"""
        self.assertTrue(math.isinf(q.use_littles_law(30, 25, 1, lq=3.2)))

    def test_use_littles_law_invalid_metric_value(self):
        """Test use_littles_law returns None for invalid metric values"""
        self.assertIsNone(q.use_littles_law(20, 25, 1, lq=math.nan))
        self.assertIsNone(q.use_littles_law(20, 25, 1, lq=math.inf))
        self.assertIsNone(q.use_littles_law(20, 25, 1, lq=-1))


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)