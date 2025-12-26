
import os
import fnmatch
import pandas as pd
import numpy as np


def combineSamples(pattern: str, path: str = ".", control_samples: int | None = None):
    """
    Combine multiple sample CSV files and split into control/test groups.

    Reads all files matching the pattern, takes the first (and only) row from each,
    combines them into a single DataFrame, and splits into control and test subsets.

    Args:
        pattern (str): Glob pattern to match filenames (e.g., "boiler_sample_*.csv")
        path (str): Directory path to search (default ".")
        control_samples (int | None): Number of control samples. If None, defaults to 60%

    Returns:
        dict: Contains pattern, path, control_samples, files, and if files found:
              filenames, samples, control, test
    """

    # list all matching files in given path
    all_files = os.listdir(path)
    paths = sorted(
        os.path.join(path, f)
        for f in all_files
        if fnmatch.fnmatch(f, pattern)
    )

    # output structure begins here
    out = {
        "pattern": pattern,
        "path": path,
    }

    # If no files match — return empty structured result
    if not paths:
        out.update({
            "filenames": [],
            "files": 0,
            "samples": pd.DataFrame(),
            "control": pd.DataFrame(),
            "test": pd.DataFrame(),
            "control_samples": 0 if control_samples is None else int(control_samples),
        })
        return out

    # load 1 row from each file
    frames = []
    for p in paths:
        df = pd.read_csv(p)
        first_col = df.columns[0]
        df = df.rename(columns={first_col: "sample"})

        # enforce column order
        cols = ["sample"] + [f"t{i}" for i in range(1, 9)]
        df = df[cols]

        # take only first row (each file contains exactly 1 sample)
        frames.append(df.iloc[[0]])

    # Concatenate and set 'sample' as index WITHOUT dropping the column
    samples = pd.concat(frames, ignore_index=True)
    samples = samples.set_index('sample', drop=False)
    # Uses sample numbers as index

    # determine control sample count
    n = len(samples)
    if control_samples is None:
        ctrl = int(np.floor(0.60 * n))  # default behavior
    else:
        ctrl = int(control_samples)

    # control + test split - keep the index intact
    control = samples.iloc[:ctrl]
    # Keeps original index
    test = samples.iloc[ctrl:]

    # fill final output
    out.update({
        "filenames": [os.path.basename(p) for p in paths],
        "files": len(paths),
        "samples": samples,
        "control": control,
        "test": test,
        "control_samples": ctrl,
    })

    return out