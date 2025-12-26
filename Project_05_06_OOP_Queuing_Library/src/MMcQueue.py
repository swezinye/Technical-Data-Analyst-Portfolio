"""
MMcQueue class - Implementation of M/M/c queue.
Multi-server: Poisson arrivals, Exponential service, c servers.

"""
from __future__ import annotations

import math
from BaseQueue import BaseQueue


class MMcQueue(BaseQueue):
    """Erlang-C implementation for M/M/c."""

    # -------------------- construction --------------------

    def __init__(self, lamda: float | tuple[float, ...], mu: float, c: int = 1) -> None:
        """
        Args:
            lamda: Aggregate arrival rate (λ). Tuples will be summed (non-priority queues).
            mu: Per-server service rate (μ).
            c: Number of servers (integer ≥ 1).
        """
        self._c: int | float = math.nan  # temp to avoid attribute errors

        if isinstance(c, (int, float)) and c >= 1 and c == int(c):
            self._c = int(c)
        else:
            self._c = math.nan

        super().__init__(lamda, mu)

    # -------------------- validation / feasibility --------------------

    def is_valid(self) -> bool:
        """True iff c is integer ≥1 and base is valid."""
        if not (isinstance(self._c, int) and self._c >= 1):
            return False
        return super().is_valid()

    def is_feasible(self) -> bool:
        """True iff ρ = λ/(c μ) < 1."""
        if not self.is_valid():
            return False
        return self.ro < 1

    # -------------------- properties --------------------

    @property
    def ro(self) -> float:
        """Per-server utilization: ρ = λ/(c μ)."""
        if not self.is_valid():
            return math.nan
        return self._lamda / (self._c * self._mu)

    @property
    def c(self) -> int | float:
        """Getter for number of servers."""
        return self._c

    @c.setter
    def c(self, value: int | float) -> None:
        """Setter for number of servers; invalid ⇒ NaN; triggers recompute."""
        if isinstance(value, (int, float)) and value >= 1 and value == int(value):
            self._c = int(value)
        else:
            self._c = math.nan
        self._recalc_needed = True

    # -------------------- metrics --------------------

    def _calc_metrics(self) -> None:
        """
        Erlang-C normalization and Lq:

            a = λ/μ
            ρ = a/c
            P0 = 1 / [ Σ_{n=0}^{c-1} a^n/n!  +  (a^c / (c!(1-ρ))) ]
            P_wait = (a^c / (c!(1-ρ))) * P0
            Lq = P_wait * ρ / (1-ρ)

        Infeasible (ρ ≥ 1): P0 = +inf, Lq = +inf.
        Invalid: P0 = NaN, Lq = NaN.
        """
        try:
            if not self.is_valid():
                self._p0 = math.nan
                self._lq = math.nan
                return

            if not self.is_feasible():
                self._p0 = math.inf
                self._lq = math.inf
                return

            lam, mu, c = self._lamda, self._mu, self._c
            a = lam / mu
            rho = a / c

            series = sum((a ** n) / math.factorial(n) for n in range(c))
            tail = (a ** c) / (math.factorial(c) * (1.0 - rho))
            self._p0 = 1.0 / (series + tail)

            p_wait = ((a ** c) / (math.factorial(c) * (1.0 - rho))) * self._p0
            self._lq = p_wait * (rho / (1.0 - rho))
        finally:
            self._recalc_needed = False

    # -------------------- representation --------------------

    def __str__(self) -> str:
        """Append c to BaseQueue string."""
        return super().__str__() + f"\n\tc: {self.c}"
