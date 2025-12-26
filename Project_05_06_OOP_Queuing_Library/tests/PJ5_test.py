# tests_project5_pytest.py
import math


from BaseQueue import BaseQueue
from MM1Queue import MM1Queue
from MMcQueue import MMcQueue


# Minimal concrete subclass so we can test BaseQueue mechanics
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


def close(a, b, r=1e-10, a_tol=0.0):
    return math.isclose(a, b, rel_tol=r, abs_tol=a_tol)


# ---------------- BaseQueue (rubric names) ----------------
def test_calc_lq():
    q = _DummyQueue(20, 25)
    lq1 = q.lq
    q.lamda = 10
    lq2 = q.lq
    assert lq2 < lq1
    q.mu = 30
    lq3 = q.lq
    assert lq3 < lq2


def test_init():
    q = _DummyQueue(12, 20)
    assert q.is_valid() and q.is_feasible()
    q2 = _DummyQueue(-5, 20)
    assert not q2.is_valid()
    assert math.isnan(q2.lq) and math.isnan(q2.p0)


def test_is_feasible():
    assert _DummyQueue(20, 25).is_feasible()
    q = _DummyQueue(30, 25)
    assert not q.is_feasible()
    assert math.isinf(q.lq) and math.isinf(q.p0)


def test_is_valid():
    assert _DummyQueue(1, 1).is_valid()
    assert not _DummyQueue(0, 1).is_valid()
    assert not _DummyQueue(1, 0).is_valid()


def test_l():
    q = _DummyQueue(20, 25)
    assert close(q.l, q.lq + (q.lamda / q.mu))
    q2 = _DummyQueue(30, 25)
    assert math.isinf(q2.l)


def test_lamda():
    q = _DummyQueue((5, 10, 5), 25)
    assert q.lamda == 20
    q2 = _DummyQueue((-1, 2, 3), 25)
    assert math.isnan(q2.lamda)


def test_lq():
    q = _DummyQueue(20, 25)
    assert q.lq >= 0
    assert math.isinf(_DummyQueue(30, 25).lq)


def test_mu():
    q = _DummyQueue(10, 20)
    q.mu = 25
    assert q.mu == 25
    q.mu = -1
    assert math.isnan(q.mu)


def test_r():
    q = _DummyQueue(20, 25)
    assert close(q.r, q.ro)


def test_ro():
    q = _DummyQueue(20, 25)
    assert close(q.ro, 0.8)


def test_w():
    q = _DummyQueue(20, 25)
    assert close(q.w, q.l / q.lamda)
    q2 = _DummyQueue(-5, 25)
    assert math.isnan(q2.w)


def test_wq():
    q = _DummyQueue(20, 25)
    assert close(q.wq, q.lq / q.lamda)
    q2 = _DummyQueue(-5, 25)
    assert math.isnan(q2.wq)


# ---------------- MM1Queue (rubric names) ----------------
def test_feasible_mm1():
    assert MM1Queue(20, 25).is_feasible()


def test_init_mm1():
    q = MM1Queue(20, 25)
    assert q.is_valid() and q.is_feasible()
    assert not MM1Queue(-1, 25).is_valid()


def test_l_mm1():
    q = MM1Queue(20, 25)
    assert close(q.l, q.lq + q.ro)


def test_lq_mm1():
    q = MM1Queue(20, 25)
    rho = 20 / 25
    assert close(q.lq, rho * rho / (1 - rho))


def test_p0_mm1():
    q = MM1Queue(20, 25)
    rho = 20 / 25
    assert close(q.p0, 1 - rho)


def test_valid_mm1():
    assert MM1Queue(1, 2).is_valid()
    assert not MM1Queue(0, 2).is_valid()
    assert not MM1Queue(1, 0).is_valid()


def test_w_mm1():
    q = MM1Queue(20, 25)
    assert close(q.w, q.l / q.lamda)


def test_wq_mm1():
    q = MM1Queue(20, 25)
    assert close(q.wq, q.lq / q.lamda)


# ---------------- MMcQueue (rubric names) ----------------
def test_feasible_mmc():
    assert MMcQueue(20, 25, 2).is_feasible()


def test_init_mmc():
    q = MMcQueue(20, 25, 3)
    assert q.is_valid() and q.is_feasible()
    assert not MMcQueue(20, 25, 0).is_valid()


def test_l_mmc():
    q = MMcQueue(20, 25, 3)
    assert close(q.l, q.lq + (q.lamda / q.mu))


def test_lq_mmc():
    assert MMcQueue(20, 25, 3).lq >= 0.0


def test_p0_mmc():
    q = MMcQueue(20, 25, 3)
    assert 0 < q.p0 <= 1


def test_valid_mmc():
    assert MMcQueue(1, 1, 1).is_valid()
    assert not MMcQueue(1, 1, 0).is_valid()


def test_w_mmc():
    q = MMcQueue(20, 25, 2)
    assert close(q.w, q.l / q.lamda)


def test_wq_mmc():
    q = MMcQueue(20, 25, 2)
    assert close(q.wq, q.lq / q.lamda)
