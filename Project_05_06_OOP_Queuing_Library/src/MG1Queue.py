
import math
from BaseQueue import BaseQueue


class MG1Queue(BaseQueue):
    """
    Pollaczek–Khinchine:
        Lq = (ρ^2 + λ^2 σ^2) / [2(1 − ρ)],  with ρ = λ/μ.
        P0 = 1 − ρ.
    """

    def __init__(self, lamda, mu, sigma):
        self._sigma = math.nan
        self.sigma = sigma  # use setter to validate; sets _recalc_needed
        super().__init__(lamda, mu)

    # ----- validity / feasibility -----

    def is_valid(self) -> bool:
        """Extend Base validity to include σ ≥ 0."""
        if not super().is_valid():
            return False
        s = self.sigma
        return isinstance(s, (int, float)) and not math.isnan(s) and s >= 0

    def is_feasible(self) -> bool:
        """
        Feasibility for M/G/1 uses only λ and μ (ρ = λ/μ < 1).
        σ is irrelevant for stability; this matches lecture tests.
        """
        if not super().is_valid():  # only λ, μ
            return False
        rho = self.lamda / self.mu
        return rho < 1.0

    # ----- property for sigma -----

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self._sigma = float(value)
        else:
            self._sigma = math.nan
        self._recalc_needed = True

    # ----- core calculations -----

    def _calc_metrics(self) -> None:
        try:
            if not self.is_valid():
                self._p0 = math.nan
                self._lq = math.nan
                return

            if not self.is_feasible():
                self._p0 = math.inf
                self._lq = math.inf
                return

            rho = self.ro             # uses getters internally
            lam = self.lamda
            sig = self.sigma
            var_s = sig * sig

            self._p0 = 1.0 - rho
            self._lq = (rho * rho + (lam * lam) * var_s) / (2.0 * (1.0 - rho))
        finally:
            self._recalc_needed = False

    def __str__(self):
        return super().__str__() + f"\n\tsigma: {self.sigma}"
