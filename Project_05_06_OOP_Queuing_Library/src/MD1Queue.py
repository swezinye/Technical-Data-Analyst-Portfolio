
import math
from BaseQueue import BaseQueue


class MD1Queue(BaseQueue):
    """Implements _calc_metrics for M/D/1."""

    def _calc_metrics(self) -> None:
        if not self.is_valid():
            self._p0 = math.nan
            self._lq = math.nan
            self._recalc_needed = False
            return

        if not self.is_feasible():
            self._p0 = math.inf
            self._lq = math.inf
            self._recalc_needed = False
            return

        rho = self.ro  # λ/μ
        # single-server empty prob same as MM1
        self._p0 = 1 - rho
        # M/D/1 queue length in line: exactly half of MM1 with same ρ
        self._lq = (rho * rho) / (2 * (1 - rho))
        self._recalc_needed = False
