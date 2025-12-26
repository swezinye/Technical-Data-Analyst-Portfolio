# test_project8.py
# Tests for Project 8: combineSamples, reformatSamples, extractCoordinates, analyzeWords
# Run with:  python -m unittest test_project8.py -v

import os
import glob
import unittest
import pandas as pd
import numpy as np

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

from combineSamples import combineSamples
from reformatSamples import reformatSamples
from extractCoordinates import extractCoordinates
from analyzeWords import analyzeWords


# ============================================================
#   TEST combineSamples
# ============================================================
class TestCombineSamples(unittest.TestCase):

    def test_combine_happy_path(self):
        pattern = "boiler_sample_*.csv"

        # deterministic list of files
        all_paths = sorted(glob.glob(os.path.join(DATA_DIR, pattern)))
        expected_n = len(all_paths)
        self.assertGreater(expected_n, 0, f"No files found matching {pattern} in {DATA_DIR}")

        res = combineSamples(pattern, path=DATA_DIR)

        # Required fields
        required = {
            "pattern", "path", "files", "control_samples",
            "filenames", "samples", "control", "test"
        }
        for k in required:
            self.assertIn(k, res, f"Missing key: {k}")

        # Count checks
        self.assertEqual(res["files"], expected_n)
        self.assertEqual(len(res["filenames"]), expected_n)

        expected_filenames = [os.path.basename(p) for p in all_paths]
        self.assertListEqual(res["filenames"], expected_filenames)

        # samples columns
        expected_cols = ["sample"] + [f"t{i}" for i in range(1, 9)]
        self.assertListEqual(list(res["samples"].columns), expected_cols)

        # control sizes
        ctrl_expect = int(np.floor(0.60 * expected_n))
        self.assertEqual(res["control_samples"], ctrl_expect)
        self.assertEqual(len(res["control"]), ctrl_expect)
        self.assertEqual(len(res["test"]), expected_n - ctrl_expect)

        # Override test
        override = 3
        res2 = combineSamples(pattern, path=DATA_DIR, control_samples=override)
        self.assertEqual(res2["control_samples"], override)
        self.assertEqual(len(res2["control"]), override)
        self.assertEqual(len(res2["test"]), expected_n - override)

    # -----------------------------------------------------------
    # FIXED VERSION — MATCHES YOUR FUNCTION'S BEHAVIOR
    # -----------------------------------------------------------
    def test_combine_no_matches(self):
        res = combineSamples("no_such_file_*.csv", path=DATA_DIR)

        # Your function always returns these keys
        expected_keys = {
            "pattern", "path", "files", "control_samples",
            "filenames", "samples", "control", "test"
        }

        for k in expected_keys:
            self.assertIn(k, res)

        # Expected values for no files
        self.assertEqual(res["files"], 0)
        self.assertEqual(res["filenames"], [])
        self.assertEqual(len(res["samples"]), 0)
        self.assertEqual(len(res["control"]), 0)
        self.assertEqual(len(res["test"]), 0)
        self.assertEqual(res["control_samples"], 0)


# ============================================================
#   TEST reformatSamples
# ============================================================
class TestReformatSamples(unittest.TestCase):

    def test_reformat_happy_path(self):
        rings = pd.read_csv(os.path.join(DATA_DIR, "pistonrings.csv"))
        wide = reformatSamples(rings)

        self.assertIsInstance(wide, pd.DataFrame)

        # sample column
        self.assertIn("sample", wide.columns[0].lower())

        # obs.# columns
        obs_cols = list(wide.columns[1:])
        self.assertGreater(len(obs_cols), 0)
        for c in obs_cols:
            self.assertRegex(c, r"^obs\.\d+$")

        # correct number of sample rows
        sample_col = next((c for c in rings.columns if c.lower() == 'sample'), rings.columns[0])
        n_samples = rings[sample_col].nunique()
        self.assertEqual(wide.shape[0], n_samples)

    def test_reformat_uneven_returns_none(self):
        df = pd.DataFrame({
            "sample": [1, 1, 2, 2, 2],   # uneven samples
            "value": [10, 11, 20, 21, 22]
        })
        out = reformatSamples(df)
        self.assertIsNone(out)


# ============================================================
#   TEST extractCoordinates
# ============================================================
class TestExtractCoordinates(unittest.TestCase):

    def test_extract_happy_path(self):
        coords = pd.read_csv(os.path.join(DATA_DIR, "coordinates.csv"))
        out = extractCoordinates(coords)

        self.assertIsInstance(out, pd.DataFrame)
        self.assertListEqual(list(out.columns), ["station", "lat", "lon"])

        self.assertTrue(pd.api.types.is_numeric_dtype(out["lat"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(out["lon"]))

        self.assertEqual(len(out), len(coords))

    def test_extract_missing_columns(self):
        df1 = pd.DataFrame({"coordinates": ["(10.5, -20.7)"]})
        self.assertEqual(extractCoordinates(df1), -1)

        df2 = pd.DataFrame({"station": ["X1", "X2"]})
        self.assertEqual(extractCoordinates(df2), -2)


# ============================================================
#   TEST analyzeWords
# ============================================================
class TestAnalyzeWords(unittest.TestCase):

    def test_analyze_happy_path(self):
        words = pd.read_csv(os.path.join(DATA_DIR, "words.csv"), header=None)[0]
        prof = analyzeWords(words)

        keys_expected = {
            "letter_counts", "max_char", "size_counts",
            "oo_count", "oo_words", "words_6plus", "words_6plus_count"
        }
        self.assertTrue(keys_expected.issubset(prof.keys()))

        # letter a–z
        alphabet = {chr(c) for c in range(ord('a'), ord('z')+1)}
        self.assertEqual(set(prof["letter_counts"].keys()), alphabet)

        # consistency checks
        self.assertEqual(prof["oo_count"], len(prof["oo_words"]))
        self.assertEqual(prof["words_6plus_count"], len(prof["words_6plus"]))

        if prof["max_char"] > 0:
            self.assertEqual(
                set(prof["size_counts"].keys()),
                set(range(1, prof["max_char"] + 1))
            )


# Run
if __name__ == "__main__":
    unittest.main(verbosity=2)
