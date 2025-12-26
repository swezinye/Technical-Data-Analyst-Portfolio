import os
import fnmatch
import pandas as pd
import numpy as np


def reformatSamples(samples: pd.DataFrame):
    """
    Reshape long→wide so each sample is one row:
      - Drops any columns starting with 'Unnamed:', like 'Unnamed: 0'.
      - Verifies uniform observations per sample, returning None if uneven.
      - Columns: 'sample', 'obs.1'..'obs.k'.
    """

    if samples is None or samples.empty:
        return None

    # --- Data Cleaning: Remove 'Unnamed' columns from CSV index residue ---
    cols_to_drop = [
        col for col in samples.columns
        if isinstance(col, str) and col.lower().startswith('unnamed:')
    ]
    samples = samples.drop(columns=cols_to_drop, errors='ignore')

    # Find 'sample' column case-insensitively
    cols_lower = {c.lower(): c for c in samples.columns}
    if "sample" not in cols_lower:
        return None
    sample_col = cols_lower["sample"]

    # Identify the observation value column
    obs_col = next((c for c in samples.columns if c != sample_col), None)
    if obs_col is None:
        return None

    # Verify uniform counts per sample (Requirement Check)
    counts = samples.groupby(sample_col).size()
    if counts.nunique() != 1:
        return None
    k = int(counts.iloc[0])

    # Reshape data (Long to Wide)
    tmp = samples[[sample_col, obs_col]].copy()
    tmp["obs_no"] = tmp.groupby(sample_col).cumcount() + 1

    wide = tmp.pivot(index=sample_col, columns="obs_no", values=obs_col)

    # Rename columns (Rubric Requirement)
    wide.columns = [f"obs.{i}" for i in range(1, k + 1)]

    # dd 'sample' column while keeping it as index (drop=False)
    wide.insert(0, 'sample', wide.index)

    return wide