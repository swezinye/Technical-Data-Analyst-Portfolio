import math
from typing import Union, List, Tuple

# function 1 is_valid
def is_valid(lamda:Union[float,int, List[Union[float,int]], Tuple[Union[float,int],...]], mu:Union[float,int], c:Union[float,int]=1)->bool:
    """
    Validate queueing system parameters.

    Central validation function ensuring all queue parameters meet mathematical requirements for
    valid queueing theory calculations.All other functions route validation through this function
    to maintain consistency.

    Args:
        lamda (float | list | tuple): arrival rate(s), must be > 0
            -Single value for standard M/M/c queues
            -List/tuple for priority queue systems wih multiple classes
        mu (float): service rates must be > 0
            Represents sever capacity (customers served per time unit)
        c (int): number of servers, must be >= 1
            -Physical servers available in the system
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


# function 2 is_feasible
def is_feasible(lamda:Union[float,int,List[Union[float,int]],Tuple[Union[float,int],...]], mu:Union[float,int], c:Union[float,int]=1)->bool:
    """
    Check if a queueing system is feasible.

    A queue is feasible when utilization ρ < 1. This ensures the system
    can handle incoming traffic without infinite queue growth over time.

    Args:
        lamda (float | list | tuple): arrival rate(s), must be > 0
        mu (float): service rates must be > 0
        c (int): number of servers, must be >= 1
    Returns:
        bool: True if feasible (p < 1), false otherwise
    """
    if not is_valid(lamda, mu, c):
        return False

    total_lamda = lamda if isinstance(lamda, (int, float)) else sum(lamda)
    ro = total_lamda / (c * mu)

    return ro < 1


# function 3 calc_p0
def calc_p0(lamda:Union[float,int,List[Union[float,int]],Tuple[Union[float,int],...]], mu:Union[float,int], c:Union[float,int]=1)->float:
    """
    Calculate P0 (probability system is empty) for M/M/c queue.

    P0 represents the steady-state probability that no customers are in the system.
    This is a fundamental metric used to derive other performance measures.

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

    total_lamda = lamda if isinstance(lamda, (int, float)) else sum(lamda)
    a = total_lamda / mu
    ro = total_lamda / (c * mu)

    if c == 1:
        return 1 - ro
    else:
        # Summation term for P0: Σ(a^n/n!) for n=0 to c-1
        series = sum([(a ** n) / math.factorial(n) for n in range(int(c))])
        
        # Tail term for P0 formula
        tail = (a ** c) / (math.factorial(int(c)) * (1 - ro))

        p0 = 1 / (series + tail)
        return p0


# function 4 calc_lq_mmc
def calc_lq_mmc(lamda:Union[float,int,List[Union[float,int]], Tuple[Union[float,int],...]], mu:Union[float,int], c:Union[float,int]=1)->float:
    """
    Calculates the average of customers in the queue for M/M/c model

    Lq represents the expected number of customers waiting for service (not being served).
    This excludes customers currently receiving service and is a key performance metric.

    Args:
        lamda (float): The arrival rate of customers
            -Single value for standard M/M/c queue
            -List/tuple for priority queues (uses aggregate behavior)
        mu (float): The service rate of customers
        c (int): Number of servers
    Returns:
        float: Average of customers in the queue (Lq).
        returns math.nan if invalid input (e.g., negative rates)
        returns math.inf for an infeasible system (rho >= 1).
    """
    if not is_valid(lamda, mu, c):
        return math.nan

    if not is_feasible(lamda, mu, c):
        return math.inf

    total_lamda = lamda if isinstance(lamda, (int, float)) else sum(lamda)
    ro = total_lamda / (c * mu)

    if c == 1:
        # M/M/1 formula
        return (ro ** 2) / (1 - ro)

    # Multi-server M/M/c formula
    a = total_lamda / mu
    p0 = calc_p0(lamda, mu, c)
    
    # Calculate Pw (Probability of waiting) and then Lq
    numerator = (a ** c) * ro
    denominator = math.factorial(int(c)) * ((1 - ro) ** 2)
    lq = (numerator / denominator) * p0
    
    return lq