import math
from pois import factorial, dpois, ppois, qpois

def run_tests():
    print("--- Starting Poisson Project Tests ---")

    # 1. Test factorial(x)
    print("\nTesting factorial(x):")
    print(f"  Valid (5!):    {factorial(5)} (Expected: 120)")
    print(f"  Base Case (0!): {factorial(0)} (Expected: 1)")
    print(f"  Non-Integer:    {factorial(5.5)} (Expected: -inf)")
    print(f"  Negative:       {factorial(-2)} (Expected: nan)")
    print(f"  Over Limit:     {factorial(1001)} (Expected: inf)")

    # 2. Test dpois(x, lamda)
    print("\nTesting dpois(x, lamda):")
    # For lamda=2, x=3, result should be approx 0.1804
    print(f"  Standard (3, 2): {dpois(3, 2):.4f} (Expected: ~0.1804)")
    print(f"  Negative x:      {dpois(-1, 2)} (Expected: 0.0)")
    print(f"  Non-integer x:   {dpois(2.5, 2)} (Expected: -inf)")

    # 3. Test ppois(x, lamda)
    print("\nTesting ppois(x, lamda):")
    # Sum of dpois for x=0,1,2 with lamda=2
    print(f"  Standard (2, 2): {ppois(2, 2):.4f} (Expected: ~0.6767)")
    print(f"  Negative x:      {ppois(-5, 2)} (Expected: 0.0)")

    # 4. Test qpois(alpha, lamda)
    print("\nTesting qpois(alpha, lamda):")
    print(f"  Inverse (0.95, 2): {qpois(0.95, 2)} (Expected: 5.0)")
    print(f"  Alpha > 1:         {qpois(1.1, 2)} (Expected: inf)")
    print(f"  Alpha < 0:         {qpois(-0.1, 2)} (Expected: -inf)")

    print("\n--- Tests Complete ---")

if __name__ == "__main__":
    run_tests()