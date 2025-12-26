"""
MM1Queue class - Implementation of M/M/1 queue.
Single-server: Poisson arrivals, Exponential service.

"""
from __future__ import annotations

import math
from BaseQueue import BaseQueue


class MM1Queue(BaseQueue):
    """Implements _calc_metrics() for M/M/1."""

    def _calc_metrics(self) -> None:
        """
        M/M/1 formulas (feasible):
            ρ = λ/μ
            P0 = 1 - ρ
            Lq = ρ^2 / (1 - ρ)

        Infeasible (ρ >= 1): P0 = +inf, Lq = +inf.
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

            rho = self.ro
            self._p0 = 1.0 - rho
            self._lq = (rho * rho) / (1.0 - rho)
        finally:
            # lecture pattern: ensure the recompute flag is always cleared
            self._recalc_needed = False
