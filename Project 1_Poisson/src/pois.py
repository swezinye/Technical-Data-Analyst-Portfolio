import math


def factorial(x):
    """
    Calculates x! using recursion.
    
    Returns:
    - -math.inf if x is not an integer
    - math.nan if x is a negative integer
    - math.inf if x > 1000 (to prevent stack overflow)
    - 1 if x = 0 (base case)
    - x * factorial(x - 1) otherwise (recursive step)
    """
    # 1. Check if x is an integer (e.g., handles 5.5 or "string")
    if not isinstance(x, int):
        return -math.inf
    
    # 2. Check if x is a negative integer
    if x < 0:
        return math.nan
    
    # 3. Check for recursion limit (assignment cap)
    if x > 1000:
        return math.inf
    
    # 4. Base Case (The Boundary Condition that stops recursion)
    if x == 0:
        return 1
    
    # 5. Recursive Step
    return x * factorial(x - 1)


def dpois(x, lamda):
    """
    Poisson probability mass function:
      f(x) = (lamda**x * exp(-lamda)) / x!

    Returns:
      - -math.inf if x is not integer
      - 0.0 if x < 0
      - math.nan if lamda < 0
    """
    if lamda < 0:
        return math.nan
    if not isinstance(x, int):
        return -math.inf
    if x < 0:
        return 0.0
    #The prompt doesn't specity an error for lamda<0
    #but math.exp(-lamda) handles it. Adding check if desired: 
    

    denom = factorial(x)
    #Using the formula:(e^-L * L^X) / X!)
    numer = math.exp(-lamda) * (lamda ** x)
    return numer / denom


def ppois(x, lamda):
    """
    Poisson cumulative distribution function:
      F(x) = sum_{c=0..x} dpois(c, lamda)

    Returns:
      - -math.inf if x is not integer
      - 0.0 if x < 0
      - math.nan if lamda < 0
    """
    
    if not isinstance(x, int):
        return -math.inf
    if x < 0:
        return 0.0

    total = 0.0
    for c in range(x + 1):
        total += dpois(c, lamda)
    return total


def qpois(alpha, lamda):
    """
    Poisson inverse CDF:
      Smallest x with P(X ≤ x) >= alpha
    """
    if alpha > 1:
        return math.inf
    if alpha < 0:
        return  -math.inf
    


    cumulative = 0.0
    x = 0
    while True:
        cumulative += dpois(x, lamda)
        if cumulative >= alpha:
            return 
        x += 1
