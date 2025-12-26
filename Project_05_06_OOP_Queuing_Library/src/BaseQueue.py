"""
BaseQueue class - Base class for all queue types.

"""
from __future__ import annotations

import math
from abc import ABC
from typing import Tuple


class BaseQueue(ABC):
    """
    Base class for queue implementations.

    Stored (private):
        _lamda (float): arrival rate λ (scalar; tuples are summed in setter)
        _mu (float): service rate μ
        _lq (float): average number in queue
        _p0 (float): probability of empty system
        _recalc_needed (bool): flag for lazy recomputation

    Derived (properties):
        ro (ρ), r (alias), utilization (alias), l, wq, w, p0, lq
    """

    # -------------------- construction --------------------

    def __init__(self, lamda: float | Tuple[float, ...], mu: float) -> None:
        """
        Initialize a BaseQueue instance.

        Args:
            lamda: Arrival rate (λ). If tuple is provided, it is summed (non-priority queues).
            mu: Service rate (μ).
        """
        # computed placeholders first
        self._lq: float = math.nan
        self._p0: float = math.nan
        self._recalc_needed: bool = True

        # storage placeholders (setters will validate)
        self._lamda: float = math.nan
        self._mu: float = math.nan

        # validate via setters (centralized validation)
        self.mu = mu
        self.lamda = lamda

        # initialize computed metrics per spec
        if self.is_valid() and self.is_feasible():
            self._calc_metrics()
        elif self.is_valid() and not self.is_feasible():
            # infeasible ⇒ both infinite (per rubric/project text)
            self._lq = math.inf
            self._p0 = math.inf
            self._recalc_needed = False

    # -------------------- helpers --------------------

    def _is_numeric(self, value: object) -> bool:
        """Return True iff value is int/float and not NaN."""
        if isinstance(value, (int, float)):
            return not (isinstance(value, float) and math.isnan(value))
        return False

    def _is_numeric_or_tuple(self, value: object) -> bool:
        """Return True iff value is numeric>0 or tuple of numeric>0."""
        if isinstance(value, tuple):
            return len(value) > 0 and all(self._is_numeric(x) and x > 0 for x in value)
        return self._is_numeric(value) and value > 0

    def _simplify_lamda(self, lamda: float | Tuple[float, ...]) -> float:
        """Sum tuple λ; otherwise return scalar λ."""
        return float(sum(lamda)) if isinstance(lamda, tuple) else float(lamda)

    # -------------------- validity / feasibility --------------------

    def is_valid(self) -> bool:
        """True iff λ>0 and μ>0 are numeric."""
        if not (isinstance(self._mu, (int, float)) and self._mu > 0):
            return False
        return isinstance(self._lamda, (int, float)) and self._lamda > 0

    def is_feasible(self) -> bool:
        """True iff ρ < 1 (uses current ro property)."""
        if not self.is_valid():
            return False
        return self.ro < 1

    # -------------------- abstract metrics --------------------


    def _calc_metrics(self) -> None:
        """
        Calculate and store Lq and P0. Derived classes implement the formulas.
        The last action of this method should be to set _recalc_needed = False.
        """
        self._lq = math.nan
        self._p0 = math.nan
        self._recalc_needed = False

    # -------------------- derived properties --------------------

    @property
    def ro(self) -> float:
        """Utilization ρ = λ/μ."""
        if not self.is_valid():
            return math.nan
        return self._lamda / self._mu

    @property
    def r(self) -> float:
        """Alias for ro (rubric includes test_r)."""
        return self.ro

    @property
    def utilization(self) -> float:
        """Alias for ro for readability."""
        return self.ro

    @property
    def lq(self) -> float:
        """Average number in queue (Lq). Lazy recompute if needed."""
        if self._recalc_needed and self.is_valid():
            self._calc_metrics()
        return self._lq

    @property
    def l(self) -> float:
        """
        Average number in system (L). For any c:
        L = Lq + λ/μ (Little’s Law with mean in service = λ/μ).
        """
        if not self.is_valid():
            return math.nan
        if not self.is_feasible():
            return math.inf
        return self.lq + (self._lamda / self._mu)

    @property
    def wq(self) -> float:
        """Average waiting time in queue: Wq = Lq / λ."""
        if not self.is_valid():
            return math.nan
        return self.lq / self._lamda

    @property
    def w(self) -> float:
        """Average time in system: W = L / λ."""
        if not self.is_valid():
            return math.nan
        return self.l / self._lamda

    @property
    def p0(self) -> float:
        """Probability of an empty system (P0). Lazy recompute if needed."""
        if self._recalc_needed and self.is_valid():
            self._calc_metrics()
        return self._p0

    # -------------------- stored properties --------------------

    @property
    def lamda(self) -> float:
        """Getter for λ (scalar)."""
        return self._lamda

    @lamda.setter
    def lamda(self, value: float | Tuple[float, ...]) -> None:
        """Setter for λ; sums tuples for non-priority queues; invalid ⇒ NaN."""
        self._lamda = self._simplify_lamda(value) if self._is_numeric_or_tuple(value) else math.nan
        self._recalc_needed = True

    @property
    def mu(self) -> float:
        """Getter for μ."""
        return self._mu

    @mu.setter
    def mu(self, value: float) -> None:
        """Setter for μ; invalid ⇒ NaN."""
        self._mu = float(value) if (self._is_numeric(value) and value > 0) else math.nan
        self._recalc_needed = True

    # -------------------- representation --------------------

    def __str__(self) -> str:
        """Formatted string of object state (uses getters to avoid stale values)."""
        result = f"{self.__class__.__name__} instance at {id(self)}\n"
        result += f"\tlamda: {self.lamda}\n"
        result += f"\tmu: {self.mu}\n"
        result += f"\tP0: {self.p0}\n"
        result += f"\tLq: {self.lq}\n"
        result += f"\tL: {self.l}\n"
        result += f"\tWq: {self.wq}\n"
        result += f"\tW: {self.w}"
        return result
