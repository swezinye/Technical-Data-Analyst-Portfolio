# Project6/MMcPriorityQueue.py
import math
from BaseQueue import BaseQueue
from MMcQueue import MMcQueue


class MMcPriorityQueue(MMcQueue):
    """
    M/M/c with non-preemptive priorities .

    Requirements satisfied:
      - Constructor signature identical to other queues: (lamda, mu, c).
        (lamda may be a scalar OR a tuple of class-arrival rates.)
      - Override lamda setter to:
          * accept a tuple (λ_1, …, λ_K),
          * validate components,
          * store the tuple in lamda_k,
          * and set aggregate lamda = sum(tuple) via the PARENT property (lazy calc).
      - Provide a lamda_k setter that simply delegates to the lamda setter.
      - No duplicate Erlang-C math: defer to parent for base metrics.
      - Getter-style access (use properties), no direct private attr pokes.
    """

    # -------------------------
    # construction (same call signature)
    # -------------------------
    def __init__(self, lamda, mu, c=1):
        # Let the parent run; our overridden lamda-setter will handle tuples.
        super().__init__(lamda, mu, c)
        # If a tuple was passed and valid, it was captured by our lamda-setter.
        # If scalar was passed, lamda_k stays None unless user sets it later.

    # -------------------------
    # lamda and lamda_k
    # -------------------------

    # Make lamda property delegate to parent for fget/fdel; override only fset.
    @property
    def lamda(self):
        return super().lamda

    @lamda.setter
    def lamda(self, value):
        """
        Accept scalar or tuple.
        - If tuple is valid (all numeric >= 0, and sum > 0), store as lamda_k
          and set lamda = sum(tuple).
        - If tuple invalid, set lamda = NaN and clear lamda_k.
        - If scalar, behave like parent but keep lamda_k = None unless user sets it.
        """
        lam_agg = math.nan
        keep_tuple = None

        if isinstance(value, tuple):
            # Validate tuple; align with tests: sum == 0 => treat as invalid for priority case.
            try:
                parts = [float(x) for x in value]
                if any(math.isnan(x) or x < 0 for x in parts):
                    raise ValueError
                total = float(sum(parts))
                if total <= 0.0:
                    raise ValueError
                lam_agg = total
                keep_tuple = tuple(value)
            except Exception:
                lam_agg = math.nan
                keep_tuple = None
        else:
            # Scalar path – defer to parent semantics, but do minimal sanitation.
            try:
                lam_agg = float(value)
                if not math.isfinite(lam_agg) or lam_agg < 0:
                    lam_agg = math.nan
            except Exception:
                lam_agg = math.nan

        # Store (or clear) the tuple first.
        # (Use a normal attribute so tests can access via property.)
        self._lamda_k = keep_tuple

        # Delegate to parent's property setter to preserve lazy computation.
        # IMPORTANT: property.__set__(instance, value) takes exactly (self, value).
        BaseQueue.lamda.__set__(self, lam_agg)

    # lamda_k as a property with a setter that delegates back to lamda
    @property
    def lamda_k(self):
        """Tuple of class arrival rates (if set/valid), else None."""
        return getattr(self, "_lamda_k", None)

    @lamda_k.setter
    def lamda_k(self, value):
        """
        Delegate to lamda setter so we reuse the exact same validation +
        aggregate logic. This keeps code non-duplicative and consistent.
        """
        # Just call through; our lamda setter handles tuples.
        self.lamda = value

    # Helper: 1-based accessor required by tests
    def get_lamda_k(self, k: int):
        t = self.lamda_k
        if not t or not isinstance(k, int) or k < 1 or k > len(t):
            return math.nan
        x = t[k - 1]
        return float(x) if isinstance(x, (int, float)) and x >= 0 else math.nan

    # -------------------------
    # validity and feasibility
    # -------------------------
    def is_valid(self) -> bool:
        """
        Valid iff parent is valid AND (if lamda_k exists) all components are >= 0.
        (Note: a tuple that failed validation already forced lamda = NaN above.)
        """
        if not super().is_valid():
            return False
        t = self.lamda_k
        if t is None:
            # Scalar lamda case is allowed; no tuple-level constraint.
            return True
        return all(isinstance(x, (int, float)) and not isinstance(x, bool) and x >= 0 for x in t)

    def is_feasible(self) -> bool:
        """Feasible iff parent utilization ρ < 1."""
        if not self.is_valid():
            return False
        return self.ro < 1.0

    # -------------------------
    # priority-class metrics (lecture approximation consistent with tests)
    # -------------------------

    def _denom(self):
        d = self.c * self.mu
        return d if (isinstance(d, (int, float)) and d > 0 and math.isfinite(d)) else math.nan

    def get_wq_k(self, k: int) -> float:
        # Guard rails
        if not self.is_valid():
            return math.nan
        if not self.is_feasible():
            return math.inf
        t = self.lamda_k
        if not t or not isinstance(k, int) or k < 1 or k > len(t):
            return math.nan

        Wq = self.wq
        if math.isnan(Wq) or math.isinf(Wq):
            return Wq

        denom = self._denom()
        if math.isnan(denom):
            return math.nan

        # cumulative utilizations (non-preemptive priority approximation)
        rho_total = self.lamda / denom
        cum_rho_km1 = sum(self.get_lamda_k(i + 1) for i in range(k - 1)) / denom
        cum_rho_k = sum(self.get_lamda_k(i + 1) for i in range(k)) / denom

        if any(math.isnan(x) for x in (rho_total, cum_rho_km1, cum_rho_k)):
            return math.nan

        a = 1.0 - cum_rho_km1
        b = 1.0 - cum_rho_k
        if a <= 0.0 or b <= 0.0:
            return math.inf

        # Matches the expected numbers when combined with base Erlang-C Wq.
        return Wq * (1.0 - rho_total) / (a * b)

    def get_w_k(self, k: int) -> float:
        wqk = self.get_wq_k(k)
        if math.isnan(wqk) or math.isinf(wqk):
            return wqk
        return wqk + 1.0 / self.mu

    def get_lq_k(self, k: int) -> float:
        wqk = self.get_wq_k(k)
        if math.isnan(wqk) or math.isinf(wqk):
            return wqk
        lam_k = self.get_lamda_k(k)
        return lam_k * wqk if not math.isnan(lam_k) else math.nan

    def get_l_k(self, k: int) -> float:
        wk = self.get_w_k(k)
        if math.isnan(wk) or math.isinf(wk):
            return wk
        lam_k = self.get_lamda_k(k)
        return lam_k * wk if not math.isnan(lam_k) else math.nan

    def get_b_k(self, k: int) -> float:
        """
        Barrier/availability factor used by the tests:
            B_k = 1 - ( sum_{j=1..k} λ_j ) / (c μ)
        """
        if not self.is_valid():
            return math.nan
        if not self.is_feasible():
            return math.inf
        t = self.lamda_k
        if not t or not isinstance(k, int) or k < 1 or k > len(t):
            return math.nan

        denom = self._denom()
        if math.isnan(denom):
            return math.nan

        cum = sum(self.get_lamda_k(i + 1) for i in range(k))
        return 1.0 - (cum / denom)
