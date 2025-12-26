"""
regress_tests.py

Project 2 tests for:
- regress(y, x): explicit loops + manual accumulators (no comps, no sum)
- regress_comp(y, x): list comprehensions + built-in aggregations

Return contract (both):
  (β0, β1) on success
  -1 length mismatch
  -2 x not iterable
  -3 y not iterable
  -4 non-numeric/NaN present, empty input, or Sxx == 0

Run (console):
    pip install pytest
    pytest regress_tests.py -v

Optional HTML report:
    pip install pytest-html
    pytest regress_tests.py --html=report.html --self-contained-html
"""

import csv
import math
import os
import pytest
from regress import regress, regress_comp

# --------------------------------------------------------------------
# CSV path — ALWAYS relative to this test file (fixes "file not found")
# --------------------------------------------------------------------
HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, "regress_data.csv")


# --------------------------------------------------------------------
# Flexible CSV loader (header optional).
# - If first row has 'x' and 'y' headers (any case), use those columns.
# - Otherwise, use first two columns.
# - Parse errors are skipped row-by-row.
# --------------------------------------------------------------------
def _load_xy_from_csv(path: str):
    x_vals, y_vals = [], []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        if not rows:
            return x_vals, y_vals

        def _is_number(s: str) -> bool:
            try:
                float(s)
                return True
            except ValueError:
                return False

        first = rows[0]
        has_header = any(not _is_number(cell) for cell in first)

        if has_header:
            header = [h.strip().lower() for h in first]
            try:
                xi = header.index("x")
                yi = header.index("y")
            except ValueError:
                xi, yi = 0, 1 if len(header) > 1 else (0, 0)
            data_rows = rows[1:]
        else:
            xi, yi = 0, 1 if len(first) > 1 else (0, 0)
            data_rows = rows

        for row in data_rows:
            try:
                x_vals.append(float(row[xi]))
                y_vals.append(float(row[yi]))
            except (ValueError, IndexError):
                # skip non-numeric or short rows
                continue

    return x_vals, y_vals


# ============================
# regress (loops only)
# ============================

def test_regress_valid_arguments():
    # Perfect line: y = 2 + 3x
    x = [0, 1, 2, 3]
    y = [2, 5, 8, 11]
    b0, b1 = regress(y, x)
    assert isinstance((b0, b1), tuple)
    assert math.isclose(b0, 2.0, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(b1, 3.0, rel_tol=1e-9, abs_tol=1e-9)


def test_regress_different_lengths():
    assert regress([1, 2, 3], [1, 2]) == -1


def test_regress_xy_not_iterable():
    # x not iterable -> -2
    assert regress([1, 2, 3], 5) == -2
    # y not iterable -> -3
    assert regress(5, [1, 2, 3]) == -3


def test_regress_xy_not_numeric():
    # non-numeric in inputs -> -4
    assert regress(['a', 2, 3], [1, 2, 3]) == -4
    # NaN present -> -4
    assert regress([1, 2, 3], [1, float('nan'), 3]) == -4
    # empty -> -4
    assert regress([], []) == -4
    # Sxx == 0 (all x equal) -> -4
    assert regress([1, 2, 3, 4], [5, 5, 5, 5]) == -4


# ============================
# regress_comp (comps + built-ins)
# ============================

def test_regress_comp_valid_arguments():
    # Perfect line: y = 2 + 3x
    x = [0, 1, 2, 3]
    y = [2, 5, 8, 11]
    b0, b1 = regress_comp(y, x)
    assert isinstance((b0, b1), tuple)
    assert math.isclose(b0, 2.0, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(b1, 3.0, rel_tol=1e-9, abs_tol=1e-9)


def test_regress_comp_different_lengths():
    assert regress_comp([1, 2, 3], [1, 2]) == -1


def test_regress_comp_xy_not_iterable():
    # x not iterable -> -2
    assert regress_comp([1, 2, 3], 5) == -2
    # y not iterable -> -3
    assert regress_comp(5, [1, 2, 3]) == -3


def test_regress_comp_xy_not_numeric():
    # non-numeric in inputs -> -4
    assert regress_comp([1, 2, 'a'], [1, 2, 3]) == -4
    # NaN present -> -4
    assert regress_comp([1, float('nan')], [1, 2]) == -4
    # empty -> -4
    assert regress_comp([], []) == -4
    # Sxx == 0 (all x equal) -> -4
    assert regress_comp([1, 2, 3, 4], [5, 5, 5, 5]) == -4


# ============================
# CSV dataset-based test
# ============================

def test_regression_on_csv_dataset():
    """
    Load regress_data.csv and verify:
      - If Sxx != 0 → both functions return (β0, β1) and agree closely
      - If Sxx == 0 → both functions return -4
    """
    assert os.path.exists(DATA_PATH), f"CSV not found at {DATA_PATH}"

    x, y = _load_xy_from_csv(DATA_PATH)

    # If dataset ends up empty after parsing -> expected -4
    if len(x) == 0 or len(y) == 0:
        assert regress(y, x) == -4
        assert regress_comp(y, x) == -4
        return

    # Decide expectation using Sxx
    n = len(x)
    xbar = sum(x) / n
    sxx = sum((xi - xbar) ** 2 for xi in x)

    if sxx == 0.0:
        # Degenerate dataset: slope undefined
        assert regress(y, x) == -4
        assert regress_comp(y, x) == -4
    else:
        # Normal dataset: both implementations should agree
        out1 = regress(y, x)
        out2 = regress_comp(y, x)
        assert isinstance(out1, tuple) and isinstance(out2, tuple)
        assert math.isclose(out1[0], out2[0], rel_tol=1e-9, abs_tol=1e-9)
        assert math.isclose(out1[1], out2[1], rel_tol=1e-9, abs_tol=1e-9)


# ============================
# Bonus: agreement on multiple small datasets
# ============================
@pytest.mark.parametrize(
    "x,y",
    [
        ([1.0, 2.0, 4.0, 5.0, 7.0], [1.5, 1.9, 3.2, 3.8, 4.2]),
        ([0, 1, 2], [1.0, 2.0, 3.0]),
        ([0.0, 1.0, 2.0], [1, 2, 3]),
    ],
)
def test_both_functions_consistent(x, y):
    out1 = regress(y, x)
    out2 = regress_comp(y, x)
    assert isinstance(out1, tuple) and isinstance(out2, tuple)
    assert math.isclose(out1[0], out2[0], rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(out1[1], out2[1], rel_tol=1e-9, abs_tol=1e-9)
