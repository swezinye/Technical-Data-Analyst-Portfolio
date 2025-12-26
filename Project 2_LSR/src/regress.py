from numbers import Number
from math import isnan
from toolz import isiterable
from typing import Tuple, Union

# Error codes:
#  -1: x,y have different lengths
#  -2: x is not iterable
#  -3: y is not iterable
#  -4: x or y contain non-numeric values, NaN, empty input, or slope undefined (Sxx == 0)

#Helper function: numeric validation

def _is_numeric(v) -> bool:
    """
    Test whether v is a valid numeric value.
    Must be an instance of number. Number
    Must not be NaN ( When float)
    Return True if valid , False otherwise

    """
    if not isinstance(v, Number):
        return False
    try:
        return not isnan(v)  # catches float ('nan')
    except TypeError:
        # Non-float Numbers (e.g., int, Fraction) are fine
        return True




#Function 1: regress(y,x)

def regress(y, x) -> Union[Tuple[float, float], int]:
    """
    Calculate least-squares regression coefficients (β0, β1) using ONLY
    explicit loops and manual accumulators: no list comprehensions and
    no built-in aggregation functions (like sum()).

    Returns:
        (β0, β1) on success
        -1 if lengths differ
        -2 if x is not iterable
        -3 if y is not iterable
        -4 if non-numeric/NaN present, empty input, or Sxx == 0 (undefined slope)

    Notes:
        Operations Management convention: ŷ_i = β0 + β1 * x_i
        R naming convention for coefficients: (β0, β1)
    """
    # Iterable checks (use toolz.isiterable as required)
    if not isiterable(x):
        return -2
    if not isiterable(y):
        return -3

    # Convert to lists
    x_list = list(x)
    y_list = list(y)

    # Length checks
    if len(x_list) != len(y_list):
        return -1

    n = len(x_list)
    if n == 0:
        return -4 #Empty input

    # Manual accumulators (no built-in aggregations)
    sum_x = 0.0
    sum_y = 0.0
    sum_xx = 0.0
    sum_xy = 0.0

#Loop over data and accumulate
    i = 0
    while i < n:
        xi = x_list[i]
        yi = y_list[i]
        #validate numeric
        if not (_is_numeric(xi) and _is_numeric(yi)):
            return -4
        #Convert to float for consistency
        fx = float(xi)
        fy = float(yi)
        #accumulate sums
        sum_x = sum_x + fx
        sum_y = sum_y + fy
        sum_xx = sum_xx + fx * fx
        sum_xy = sum_xy + fx * fy

        i = i + 1

    # Compute Means (still only with our accumulators)
    xbar = sum_x / n
    ybar = sum_y / n

    # Compute Centered sums identity (no built-in aggregations)
    Sxx = sum_xx - n * xbar * xbar
    Sxy = sum_xy - n * xbar * ybar

    #Check for undefined slope
    if Sxx == 0.0:
        # All x equal → slope undefined
        return -4

    #Regression coefficients
    beta_1 = Sxy / Sxx
    beta_0 = ybar - beta_1 * xbar
    return (beta_0, beta_1) # return result

#Function 2: regress_comp(y,x)
def regress_comp(y, x) -> Union[Tuple[float, float], int]:
    """
    Calculate least-squares regression coefficients (β0, β1) using
    LIST COMPREHENSIONS and built-in aggregations (like sum()).

    Returns:
        (β0, β1) on success
        -1 if lengths differ
        -2 if x is not iterable
        -3 if y is not iterable
        -4 if non-numeric/NaN present, empty input, or Sxx == 0 (undefined slope)

    Notes:
        Operations Management convention: ŷ_i = β0 + β1 * x_i
        R naming convention for coefficients: (β0, β1)
    """
    # Iterable checks (toolz.isiterable)
    if not isiterable(x):
        return -2
    if not isiterable(y):
        return -3

    x_list = list(x)
    y_list = list(y)

    if len(x_list) != len(y_list):
        return -1

    n = len(x_list)
    if n == 0:
        return -4

    # Validate numeric (reject NaN) with comprehensions allowed
    if any((not _is_numeric(v)) for v in [*x_list, *y_list]):
        return -4

    # Cast to floats with list comprehensions
    xf = [float(v) for v in x_list]
    yf = [float(v) for v in y_list]

    # Compute means using Built-in aggregations
    #x̄ = (Σ xᵢ)/n,   ȳ = (Σ yᵢ)/n
    xbar = sum(xf) / n
    ybar = sum(yf) / n
    #compute centered sums with comprehensions
    #Sxx = Σ (xᵢ − x̄)²
    # Sxy = Σ (xᵢ − x̄)(yᵢ − ȳ)
    Sxx = sum((xi - xbar) ** 2 for xi in xf)
    Sxy = sum((xi - xbar) * (yi - ybar) for xi, yi in zip(xf, yf))
    #check for undefined slope
    if Sxx == 0.0:
        return -4
    # Regression coefficients
    beta_1 = Sxy / Sxx
    beta_0 = ybar - beta_1 * xbar
    return (beta_0, beta_1) # Return result
