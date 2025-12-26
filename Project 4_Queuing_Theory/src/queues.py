import math
from typing import Union, List, Tuple

# --- Function 1: is_valid ---
def is_valid(lamda: Union[float, int, List[Union[float, int]], Tuple[Union[float, int], ...]], mu: Union[float, int],
             c: Union[float, int] = 1) -> bool:
    """
    Validate queueing system parameters.

    Args:
        lamda (float | list | tuple): arrival rate(s), must be > 0
        mu (float): service rates must be > 0
        c (int): number of servers, must be >= 1
    Returns:
        bool: True if valid, false if otherwise
    """
    # Service rate validation
    if not (isinstance(mu, (int, float)) and mu > 0):
        return False

    # Server count validation
    if not (isinstance(c, (int, float)) and c >= 1 and c == int(c)):
        return False

    # Arrival rate validation
    if isinstance(lamda, (int, float)):
        return lamda > 0

    if isinstance(lamda, (list, tuple)) and len(lamda) > 0:
        return all(isinstance(x, (int, float)) and x > 0 for x in lamda)

    return False


# --- Function 2: is_feasible ---
def is_feasible(lamda: Union[float, int, List[Union[float, int]], Tuple[Union[float, int], ...]], mu: Union[float, int],
                c: Union[float, int] = 1) -> bool:
    """
    Check if a queueing system is feasible (ρ < 1).

    Args:
        lamda (float | list | tuple): arrival rate(s), must be > 0
        mu (float): service rates must be > 0
        c (int): number of servers, must be >= 1
    Returns:
        bool: True if feasible (ρ < 1), false otherwise
    """
    if not is_valid(lamda, mu, c):
        return False

    total_lamda = _get_total_lamda(lamda)
    ro = total_lamda / (c * mu)
    return ro < 1


# --- Function 3: calc_p0 ---
def calc_p0(lamda: Union[float, int, List[Union[float, int]], Tuple[Union[float, int], ...]], mu: Union[float, int],
            c: Union[float, int] = 1) -> float:
    """
    Calculate P0 (probability system is empty) for M/M/c queue.

    Args:
        lamda (float | list): arrival rate(s)
        mu (float): service rate
        c (int): number of servers

    Returns:
        float: P0 (0 <= P0 <= 1),
               math.nan if invalid input,
               math.inf if infeasible (ρ >= 1).
    """
    if not is_valid(lamda, mu, c):
        return math.nan

    if not is_feasible(lamda, mu, c):
        return math.inf

    total_lamda = _get_total_lamda(lamda)
    a, ro = total_lamda / mu, total_lamda / (c * mu)

    if c == 1:
        return 1 - ro
    else:
        series = sum([(a ** n) / math.factorial(n) for n in range(int(c))])
        tail = (a ** c) / (math.factorial(int(c)) * (1 - ro))
        return 1 / (series + tail)


# --- Function 4: calc_lq_mmc ---
def calc_lq_mmc(lamda: Union[float, int, List[Union[float, int]], Tuple[Union[float, int], ...]], mu: Union[float, int],
                c: Union[float, int] = 1) -> float:
    """
    Calculates the average number of customers in the queue for M/M/c model

    Args:
        lamda (float): The arrival rate of customers
        mu (float): The service rate of customers
        c (int): Number of servers
    Returns:
        float: Average number of customers in the queue (Lq).
        returns math.nan if invalid input
        returns math.inf for an infeasible system (rho >= 1).
    """
    if not is_valid(lamda, mu, c):
        return math.nan

    if not is_feasible(lamda, mu, c):
        return math.inf

    total_lamda = _get_total_lamda(lamda)

    if c == 1:
        # Project 4 requirement: Specific M/M/1 Lq formula
        return (total_lamda ** 2) / (mu * (mu - total_lamda))

    a, ro = total_lamda / mu, total_lamda / (c * mu)
    p0 = calc_p0(lamda, mu, c)
    
    pw = ((a ** c) / (math.factorial(int(c)) * (1 - ro))) * p0
    return pw * ro / (1 - ro)


# --- Internal Helper Functions ---
def _get_total_lamda(lamda):
    """Calculates the total arrival rate from the lamda input."""
    if isinstance(lamda, dict):
        return sum(lamda.values())
    elif isinstance(lamda, (list, tuple)):
        return sum(lamda)
    else:
        return lamda

def _calc_utilization(total_lamda, mu, c):
    """Calculates traffic intensity (r) and server utilization (rho)."""
    r = total_lamda / mu
    ro = r / c
    return r, ro


# --- Function 5: calc_bk_mmc ---
def calc_bk_mmc(k, lamda, mu, c=1):
    """
    Calculates B_k for M/M/c/priority system using the formula:
    B_k = 1 - sum(lambda_j / (c*mu)) for j=1 to k, where B_0 = 1

    Args:
        k (int): The priority class (must be an integer >= 0).
        lamda (float or list): The average arrival rate(s)
        mu (float): The average customer service rate (must be > 0)
        c (int): Number of servers (must be an integer > 0).
    """
    if not is_valid(lamda, mu, c) or not isinstance(k, int) or k < 0:
        return math.nan

    if not is_feasible(lamda, mu, c):
        return math.inf

    lamda_list = [lamda] if isinstance(lamda, (int, float)) else list(lamda)

    if len(lamda_list) == 1 and k > 1:
        return math.nan

    # B_k = 1 - sum(lambda_j / (c*mu)) using list comprehension as required
    # B_0 returns 1.0; B_k returns the utilization complement
    return 1.0 - sum(lamda_list[j] / (c * mu) for j in range(min(k, len(lamda_list))))


# --- Function 6: calc_wqk_mmc ---
def calc_wqk_mmc(k, lamda, mu, c):
    """
    Calculates the average wait time in queue (Wq) for priority k in an M/M/c system.
    Uses the formula: W_q,k = (1-ρ)W_q / (B_{k-1} × B_k)
    """
    if not is_valid(lamda, mu, c):
        return math.nan

    lamda_tuple = (lamda,) if isinstance(lamda, (int, float)) else tuple(lamda)
    if not (isinstance(k, int) and 1 <= k <= len(lamda_tuple)):
        return math.nan

    if not is_feasible(lamda, mu, c):
        return math.inf

    total_lamda = sum(lamda_tuple)
    ro = total_lamda / (c * mu)
    lq_total = calc_lq_mmc(lamda_tuple, mu, c)
    wq_total = lq_total / total_lamda if total_lamda > 0 else 0.0

    b_k_minus_1 = calc_bk_mmc(k - 1, lamda_tuple, mu, c)
    b_k = calc_bk_mmc(k, lamda_tuple, mu, c)

    return ((1 - ro) * wq_total) / (b_k_minus_1 * b_k)


# --- Function 7: calc_lqk_mmc ---
def calc_lqk_mmc(k, lamda, wqk, c=1):
    """
    Calculates the average queue length for a specific priority class k (Lqk).
    """
    if not isinstance(lamda, (list, tuple)) or len(lamda) == 0:
        return math.nan
    if not (isinstance(k, int) and 1 <= k <= len(lamda)):
        return math.nan
    if not (isinstance(wqk, (int, float)) and wqk >= 0):
        return math.nan

    return lamda[k - 1] * wqk


# --- Function 8: use_littles_law ---
def use_littles_law(lamda, mu, c=1, **kwargs):
    """
    Calculates L, Lq, W, and Wq for a queuing system given one of these metrics.
    Accepts the first kwarg and returns a dictionary of results.
    """
    # 1. First, check if any keyword arguments were actually provided
    if not kwargs or len(kwargs) == 0:
        return None

    # 2. Validate basic parameters
    if not is_valid(lamda, mu, c):
        return math.nan
    if not is_feasible(lamda, mu, c):
        return math.inf

    # Extract first metric
    given_metric, given_value = list(kwargs.items())[0]
    
    # Check for invalid values (None, NaN, Inf, or negative)
    if not isinstance(given_value, (int, float)) or \
       math.isnan(given_value) or math.isinf(given_value) or \
       given_value < 0:
        return None

    total_lamda = _get_total_lamda(lamda)
    r, ro = _calc_utilization(total_lamda, mu, c)

    # Derive all 4 metrics based on Little's Law
    if given_metric == 'lq':
        lq = given_value
        wq = lq / total_lamda if total_lamda > 0 else 0
        w = wq + (1 / mu)
        l = total_lamda * w
    elif given_metric == 'wq':
        wq = given_value
        lq = total_lamda * wq
        w = wq + (1 / mu)
        l = total_lamda * w
    elif given_metric == 'l':
        l = given_value
        w = l / total_lamda if total_lamda > 0 else 0
        wq = w - (1 / mu)
        lq = total_lamda * wq
    elif given_metric == 'w':
        w = given_value
        l = total_lamda * w
        wq = w - (1 / mu)
        lq = total_lamda * wq

    result_dict = {'l': l, 'lq': lq, 'w': w, 'wq': wq, 'r': r, 'ro': ro}

    # Handle Priority Queue metrics (tuple return required for tests)
    if isinstance(lamda, (list, tuple)) and len(lamda) > 1:
        wqk_vals = tuple(calc_wqk_mmc(i + 1, lamda, mu, c) for i in range(len(lamda)))
        lqk_vals = tuple(calc_lqk_mmc(i + 1, lamda, wqk_vals[i]) for i in range(len(lamda)))
        result_dict['wqk'] = wqk_vals
        result_dict['lqk'] = lqk_vals

    return result_dict