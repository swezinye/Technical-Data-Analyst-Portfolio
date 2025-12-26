import math
import unittest

# Import the functions from queues.py file
from queues import is_valid, is_feasible, calc_p0, calc_lq_mmc


class TestQueuingFunctions(unittest.TestCase):
    """Comprehensive test suite for queueing theory functions"""

    def test_is_valid_basic_cases(self):
        """Test is_valid function with basic valid cases"""
        # Valid single lambda
        self.assertTrue(is_valid(5.0, 3.0, 1))
        self.assertTrue(is_valid(10, 12, 2))

        # Valid lambda list
        self.assertTrue(is_valid([2, 3, 4], 10, 3))
        self.assertTrue(is_valid((1.5, 2.5), 8, 2))

    def test_is_valid_invalid_lambda(self):
        """Test is_valid with invalid lambda values"""
        # Negative lambda
        self.assertFalse(is_valid(-5, 3, 1))
        self.assertFalse(is_valid([-1, 2], 5, 2))

        # Zero lambda
        self.assertFalse(is_valid(0, 5, 1))
        self.assertFalse(is_valid([1, 0, 3], 8, 3))

        # Empty list
        self.assertFalse(is_valid([], 5, 1))

        # Non-numeric lambda - using positional arguments to avoid type warnings
        result1 = is_valid("5", 3, 1) #String lambda
        self.assertFalse(result1)
        result2 = is_valid([1, "2"], 5, 2)
        self.assertFalse(result2)

    def test_is_valid_invalid_mu(self):
        """Test is_valid with invalid mu values"""
        # Negative mu
        self.assertFalse(is_valid(5, -3, 1))

        # Zero mu
        self.assertFalse(is_valid(5, 0, 1))

        # Non-numeric mu - using positional arguments
        result = is_valid(5, "3", 1) #String mu
        self.assertFalse(result)

    def test_is_valid_invalid_c(self):
        """Test is_valid with invalid server count"""
        # Zero servers
        self.assertFalse(is_valid(5, 3, 0))

        # Negative servers
        self.assertFalse(is_valid(5, 3, -1))

        # Non-integer servers (but float whole numbers should work)
        self.assertTrue(is_valid(5, 3, 2.0))  # Should work
        self.assertFalse(is_valid(5, 3, 2.5))  # Should fail

    def test_is_feasible_valid_cases(self):
        """Test is_feasible with feasible systems"""
        # M/M/1 feasible (ρ < 1)
        self.assertTrue(is_feasible(8, 10, 1))  # ρ = 0.8

        # M/M/c feasible
        self.assertTrue(is_feasible(10, 6, 2))  # ρ = 10/(2*6) = 0.833

        # Lambda list feasible
        self.assertTrue(is_feasible([2, 3, 4], 10, 1))  # total_λ=9, ρ=0.9

    def test_is_feasible_infeasible_cases(self):
        """Test is_feasible with infeasible systems"""
        # M/M/1 infeasible (ρ >= 1)
        self.assertFalse(is_feasible(12, 10, 1))  # ρ = 1.2
        self.assertFalse(is_feasible(10, 10, 1))  # ρ = 1.0 (boundary case)

        # M/M/c infeasible
        self.assertFalse(is_feasible(15, 6, 2))  # ρ = 15/(2*6) = 1.25

    def test_is_feasible_invalid_input(self):
        """Test is_feasible with invalid inputs"""
        self.assertFalse(is_feasible(-5, 10, 1))
        self.assertFalse(is_feasible(5, -10, 1))
        self.assertFalse(is_feasible(5, 10, 0))

    def test_calc_p0_mm1_cases(self):
        """Test calc_p0 for M/M/1 queues"""
        # Standard M/M/1 case
        p0 = calc_p0(8, 10, 1)
        expected = 1 - (8 / 10)  # 1 - ρ = 0.2
        self.assertAlmostEqual(p0, expected, places=6)

        # Another M/M/1 case
        p0 = calc_p0(5, 12, 1)
        expected = 1 - (5 / 12)  # ≈ 0.583
        self.assertAlmostEqual(p0, expected, places=6)

    def test_calc_p0_mmc_cases(self):
        """Test calc_p0 for M/M/c queues"""
        # M/M/2 case: λ=10, μ=6, c=2
        p0 = calc_p0(10, 6, 2)
        # Manual calculation for verification
        a = 10 / 6  # ≈ 1.667
        ro = 10 / (2 * 6)  # ≈ 0.833
        series = 1 + a  # 1 + 1.667 = 2.667
        tail = (a ** 2) / (math.factorial(2) * (1 - ro))  # (1.667^2)/(2 * 0.167) ≈ 8.333
        expected = 1 / (series + tail)  # 1/(2.667 + 8.333) = 1/11 ≈ 0.091
        self.assertAlmostEqual(p0, expected, places=3)

    def test_calc_p0_edge_cases(self):
        """Test calc_p0 edge cases"""
        # Invalid input should return nan
        self.assertTrue(math.isnan(calc_p0(-5, 10, 1)))
        self.assertTrue(math.isnan(calc_p0(5, -10, 1)))

        # Infeasible system should return inf
        self.assertTrue(math.isinf(calc_p0(12, 10, 1)))
        self.assertTrue(math.isinf(calc_p0(15, 6, 2)))

    def test_calc_p0_lambda_list(self):
        """Test calc_p0 with lambda as a list"""
        # Test with lambda list
        p0 = calc_p0([2, 3, 4], 10, 1)  # total_λ = 9
        expected = 1 - (9 / 10)  # 0.1
        self.assertAlmostEqual(p0, expected, places=6)

    def test_calc_lq_mmc_mm1_cases(self):
        """Test calc_lq_mmc for M/M/1 queues"""
        # Standard M/M/1: λ=10, μ=12
        lq = calc_lq_mmc(10, 12, 1)
        ro = 10 / 12  # ≈ 0.833
        expected = (ro ** 2) / (1 - ro)  # ≈ 4.167
        self.assertAlmostEqual(lq, expected, places=3)

        # Another M/M/1 case
        lq = calc_lq_mmc(8, 10, 1)
        ro = 8 / 10  # 0.8
        expected = (ro ** 2) / (1 - ro)  # 0.64/0.2 = 3.2
        self.assertAlmostEqual(lq, expected, places=6)

    def test_calc_lq_mmc_mmc_cases(self):
        """Test calc_lq_mmc for M/M/c queues"""
        # M/M/2 case: λ=10, μ=6, c=2
        lq = calc_lq_mmc(10, 6, 2)
        # This should give a finite positive value
        self.assertGreater(lq, 0)
        self.assertLess(lq, math.inf)

        # Verify it's reasonable
        self.assertGreater(lq, 0)

    def test_calc_lq_mmc_edge_cases(self):
        """Test calc_lq_mmc edge cases"""
        # Invalid input should return nan
        self.assertTrue(math.isnan(calc_lq_mmc(-5, 10, 1)))
        self.assertTrue(math.isnan(calc_lq_mmc(5, -10, 1)))
        self.assertTrue(math.isnan(calc_lq_mmc(5, 10, 0)))

        # Infeasible system should return inf
        self.assertTrue(math.isinf(calc_lq_mmc(12, 10, 1)))
        self.assertTrue(math.isinf(calc_lq_mmc(15, 6, 2)))

    def test_calc_lq_mmc_lambda_list(self):
        """Test calc_lq_mmc with lambda as a list"""
        # Test with lambda list for M/M/1
        lq = calc_lq_mmc([3, 4, 3], 12, 1)  # total_λ = 10
        ro = 10 / 12  # ≈ 0.833
        expected = (ro ** 2) / (1 - ro)
        self.assertAlmostEqual(lq, expected, places=3)

    def test_boundary_cases(self):
        """Test boundary cases where ρ approaches 1"""
        # Very close to unstable but still feasible
        lq = calc_lq_mmc(9.99, 10, 1)
        self.assertGreater(lq, 0)
        self.assertLess(lq, math.inf)

        # At the boundary (should be infeasible)
        lq = calc_lq_mmc(10, 10, 1)
        self.assertTrue(math.isinf(lq))

    def test_known_textbook_examples(self):
        """Test against known textbook examples"""
        # Example 1: M/M/1 with λ=4, μ=5
        lq = calc_lq_mmc(4, 5, 1)
        ro = 4 / 5  # 0.8
        expected = (ro ** 2) / (1 - ro)  # 0.64/0.2 = 3.2
        self.assertAlmostEqual(lq, expected, places=6)

        # Example 2: M/M/2 with λ=8, μ=5 (so total service rate = 10)
        lq = calc_lq_mmc(8, 5, 2)
        self.assertGreater(lq, 0)
        self.assertLess(lq, math.inf)

    def test_integration_all_functions(self):
        """Integration test using all functions together"""
        # Test a complete workflow
        lamda, mu, c = 10, 6, 2

        # Should be valid
        self.assertTrue(is_valid(lamda, mu, c))

        # Should be feasible
        self.assertTrue(is_feasible(lamda, mu, c))

        # P0 should be valid
        p0 = calc_p0(lamda, mu, c)
        self.assertGreater(p0, 0)
        self.assertLessEqual(p0, 1)

        # Lq should be finite and positive
        lq = calc_lq_mmc(lamda, mu, c)
        self.assertGreater(lq, 0)
        self.assertLess(lq, math.inf)


def run_manual_tests():
    """Run manual tests to verify specific calculations"""
    print("=== Manual Test Results ===")

    # Test the examples from the original code
    print("\n1. M/M/1 Example (λ=10, μ=12, c=1):")
    lq_1 = calc_lq_mmc(10, 12, 1)
    print(f"   Lq = {lq_1:.4f}")
    expected_ro = 10 / 12
    expected_lq = (expected_ro ** 2) / (1 - expected_ro)
    print(f"   Expected ρ = {expected_ro:.4f}")
    print(f"   Expected Lq = {expected_lq:.4f}")

    print("\n2. M/M/c Example (λ=10, μ=6, c=2):")
    lq_2 = calc_lq_mmc(10, 6, 2)
    print(f"   Lq = {lq_2:.4f}")
    utilization = 10 / (2 * 6)
    print(f"   ρ = {utilization:.4f}")

    print("\n3. Unstable System Example (λ=15, μ=6, c=2):")
    lq_inf = calc_lq_mmc(15, 6, 2)
    print(f"   Lq = {lq_inf}")
    unstable_ro = 15 / (2 * 6)
    print(f"   ρ = {unstable_ro:.4f} (> 1, hence unstable)")

    print("\n4. Invalid Input Example (λ=-5, μ=10, c=1):")
    lq_nan = calc_lq_mmc(-5, 10, 1)
    print(f"   Lq = {lq_nan}")

    print("\n5. P0 Calculations:")
    print(f"   P0 for M/M/1 (λ=8, μ=10): {calc_p0(8, 10, 1):.4f}")
    print(f"   P0 for M/M/2 (λ=10, μ=6): {calc_p0(10, 6, 2):.4f}")

    print("\n6. Validation Tests:")
    print(f"   is_valid(10, 12, 1): {is_valid(10, 12, 1)}")
    print(f"   is_valid(-5, 12, 1): {is_valid(-5, 12, 1)}")
    print(f"   is_feasible(10, 12, 1): {is_feasible(10, 12, 1)}")
    print(f"   is_feasible(15, 10, 1): {is_feasible(15, 10, 1)}")


if __name__ == "__main__":
    # Run the manual tests first
    run_manual_tests()

    print("\n" + "=" * 50)
    print("Running Unit Tests...")
    print("=" * 50)

    # Run the unit tests
    unittest.main(verbosity=2)