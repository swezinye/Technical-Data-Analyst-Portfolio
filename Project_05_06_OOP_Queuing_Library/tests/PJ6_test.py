# tests_project6_pytest.py
import math
import pytest

from BaseQueue import BaseQueue
from MM1Queue import MM1Queue
from MMcQueue import MMcQueue
from MD1Queue import MD1Queue
from MG1Queue import MG1Queue
from MMcPriorityQueue import MMcPriorityQueue


# -------- helpers --------

def close(a, b, rel=1e-10, abs_tol=0.0):
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_tol)


# A tiny concrete subclass for BaseQueue mechanics (no new API)
class _DummyQueue(BaseQueue):
    def _calc_metrics(self):
        if not self.is_valid():
            self._p0 = math.nan
            self._lq = math.nan
        elif not self.is_feasible():
            self._p0 = math.inf
            self._lq = math.inf
        else:
            rho = self.ro
            self._p0 = 1 - rho
            self._lq = (rho * rho) / (1 - rho)
        self._recalc_needed = False


# ============================================================
# BaseQueue (resubmit) — rubric names
# ============================================================

def test_base_test_calc_lq():
    q = _DummyQueue(20, 25)
    lq1 = q.lq
    q.lamda = 10
    assert q.lq < lq1
    q.mu = 30
    assert q.lq < (rho := (10/30))**2/(1-rho)

def test_base_test_init_and_validity():
    q = _DummyQueue(12, 20)
    assert q.is_valid() and q.is_feasible()
    q2 = _DummyQueue(-5, 20)
    assert not q2.is_valid()
    assert math.isnan(q2.lq) and math.isnan(q2.p0)

def test_base_test_is_feasible():
    assert _DummyQueue(20, 25).is_feasible()
    q = _DummyQueue(30, 25)
    assert not q.is_feasible()
    assert math.isinf(q.lq) and math.isinf(q.p0)

def test_base_test_l_w_wq_ro_alias():
    q = _DummyQueue(20, 25)
    assert close(q.l, q.lq + q.lamda / q.mu)
    assert close(q.w, q.l / q.lamda)
    assert close(q.wq, q.lq / q.lamda)
    assert close(q.r, q.ro)

def test_base_test_lamda_mu_setters_tuple_sum():
    q = _DummyQueue((5, 10, 5), 25)
    assert q.lamda == 20
    q.mu = -1
    assert math.isnan(q.mu)


# ============================================================
# MM1Queue (resubmit)
# ============================================================

def test_mm1_formulas():
    q = MM1Queue(20, 25)  # rho = 0.8
    rho = 20/25
    assert q.is_valid() and q.is_feasible()
    assert close(q.p0, 1 - rho)
    assert close(q.lq, rho*rho/(1-rho))
    assert close(q.l, q.lq + rho)
    assert close(q.wq, q.lq / q.lamda)
    assert close(q.w, q.l / q.lamda)

def test_mm1_infeasible():
    q = MM1Queue(30, 25)
    assert q.is_valid() and not q.is_feasible()
    assert math.isinf(q.lq) and math.isinf(q.p0)
    assert math.isinf(q.l)


# ============================================================
# MMcQueue (resubmit)
# ============================================================

def test_mmc_feasible_and_monotone_c():
    lam, mu = 20, 25
    q2 = MMcQueue(lam, mu, 2)  # rho = 20/(2*25)=0.4
    q3 = MMcQueue(lam, mu, 3)  # lower rho -> lower Lq
    assert q2.is_valid() and q2.is_feasible()
    assert q3.is_valid() and q3.is_feasible()
    assert q3.lq <= q2.lq

def test_mmc_infeasible():
    q = MMcQueue(30, 10, 2)  # capacity 20 < 30
    assert q.is_valid() and not q.is_feasible()
    assert math.isinf(q.lq) and math.isinf(q.p0)

def test_mmc_c_setter_and_ro():
    q = MMcQueue(20, 25, 2)
    rho2 = 20/(2*25)
    assert close(q.ro, rho2)
    q.c = 4
    assert close(q.ro, 20/(4*25))


# ============================================================
# MD1Queue (new)
# ============================================================

def test_md1_reduces_half_mm1_lq():
    lam, mu = 20, 25
    rho = lam/mu
    mm1 = MM1Queue(lam, mu)
    md1 = MD1Queue(lam, mu)
    exp_md1_lq = (rho*rho) / (2*(1-rho))
    assert md1.is_valid() and md1.is_feasible()
    assert close(mm1.lq, 2*md1.lq)
    assert close(md1.lq, exp_md1_lq)
    assert close(md1.wq, md1.lq / lam)
    assert close(md1.w, md1.l / lam)


# ============================================================
# MG1Queue (new)
# ============================================================

def test_mg1_matches_mm1_when_var_equals_exp_var():
    lam, mu = 20, 25
    rho = lam/mu
    var_exp = 1/(mu*mu)  # Var(Exp(mu)) = 1/mu^2
    mg1 = MG1Queue(lam, mu, var_exp)
    mm1 = MM1Queue(lam, mu)
    # PK: Lq = (lambda^2*Var(S) + rho^2) / (2*(1-rho))
    exp_lq = (lam*lam*var_exp + rho*rho) / (2*(1-rho))
    assert close(mg1.lq, exp_lq)
    assert close(mg1.lq, mm1.lq)  # should equal MM1 for exp variance

def test_mg1_matches_md1_when_var_zero():
    lam, mu = 20, 25
    rho = lam/mu
    mg1 = MG1Queue(lam, mu, 0.0)   # Var(S)=0 => deterministic service
    md1 = MD1Queue(lam, mu)
    exp_lq_md1 = (rho*rho)/(2*(1-rho))
    assert close(mg1.lq, exp_lq_md1)
    assert close(mg1.lq, md1.lq)


# ============================================================
# MMcPriorityQueue (new)
# ============================================================

def test_mmc_priority_basic_properties_and_sums():
    # 3 classes, c=2, feasible (lambda_total=16, capacity=20)
    lam_tuple = (6.0, 6.0, 4.0)
    mu, c = 10.0, 2
    q = MMcPriorityQueue(lam_tuple, mu, c)
    assert q.is_valid() and q.is_feasible()

    # get_lamda_k(None) should return tuple; each k returns scalar
    lam_all = q.get_lamda_k()
    assert isinstance(lam_all, tuple) and len(lam_all) == 3
    assert q.get_lamda_k(1) == lam_tuple[0]
    assert q.get_lamda_k(2) == lam_tuple[1]
    assert q.get_lamda_k(3) == lam_tuple[2]

    # sums over classes should match aggregate L and Lq
    lq_sum = sum(q.get_lq_k(k) for k in (1, 2, 3))
    l_sum = sum(q.get_l_k(k) for k in (1, 2, 3))
    assert close(lq_sum, q.lq, rel=1e-7)
    assert close(l_sum, q.l, rel=1e-7)

    # Little's Law per class
    for k in (1, 2, 3):
        lamk = q.get_lamda_k(k)
        assert close(q.get_wq_k(k), q.get_lq_k(k) / lamk)
        assert close(q.get_w_k(k), q.get_l_k(k) / lamk)

def test_mmc_priority_priority_ordering():
    lam_tuple = (6.0, 6.0, 4.0)
    q = MMcPriorityQueue(lam_tuple, 10.0, 2)
    # Higher priority (smaller k) should have shorter waits
    wq1 = q.get_wq_k(1)
    wq2 = q.get_wq_k(2)
    wq3 = q.get_wq_k(3)
    assert wq1 <= wq2 <= wq3

def test_mmc_priority_infeasible_and_invalid():
    # infeasible: total 22 > c*mu=20
    q_bad = MMcPriorityQueue((8.0, 8.0, 6.0), 10.0, 2)
    assert q_bad.is_valid() and not q_bad.is_feasible()
    assert math.isinf(q_bad.lq) and math.isinf(q_bad.p0)

    # invalid c
    q_inv = MMcPriorityQueue((6.0, 6.0, 4.0), 10.0, 0)
    assert not q_inv.is_valid()
