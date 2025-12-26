import unittest
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import os
from datavis import graph_deaths_by_state,graph_deaths_over_time,graph_oregon_death_freq

# ASSUMPTION: The functions (graph_deaths_by_state, graph_deaths_over_time,
# graph_oregon_death_freq) are available in the scope.


class TestCovidGraphs(unittest.TestCase):

    def setUp(self):
        """
        Create a synthetic DataFrame to use for all tests.
        This ensures tests are fast and don't rely on the external CSV file.
        """
        # Create 100 days of data
        dates = pd.date_range(start='2020-01-01', periods=100)

        # Create data for two states: OR and CA
        # We'll make 'OR' have specific values to test the histogram logic
        data = {
            'submission_date': dates,
            'state': ['OR', 'CA'] * 50,  # Alternating states
            'new_death': [x for x in range(100)],  # Deaths: 0, 1, 2... 99
            # Note: new_death for OR will be even numbers: 0, 2, 4... 98
            # Note: new_death for CA will be odd numbers: 1, 3, 5... 99
        }
        self.test_df = pd.DataFrame(data)

        # Ensure cleanup of files before starting
        self.files_to_check = ['deaths_by_state.png', 'OR_death_freq.png', 'deaths_over_time.png']
        for f in self.files_to_check:
            if os.path.exists(f):
                os.remove(f)

    def tearDown(self):
        """Clean up any files created during testing."""
        for f in self.files_to_check:
            if os.path.exists(f):
                os.remove(f)

    def test_by_state_hist(self):
        """
        Tests the DataFrame returned by graph_deaths_by_state.
        Verifies column names and calculation logic.
        """
        result = graph_deaths_by_state(self.test_df)

        # Check DataFrame structure
        self.assertIsInstance(result, pd.DataFrame)
        self.assertListEqual(sorted(result.columns.tolist()), ['state', 'tot_death'])

        # Check Values
        # OR deaths should be sum of 0, 2, ..., 98
        expected_or_sum = sum(range(0, 100, 2))
        actual_or_sum = result.loc[result['state'] == 'OR', 'tot_death'].values[0]
        self.assertEqual(actual_or_sum, expected_or_sum)

        # CA deaths should be sum of 1, 3, ..., 99
        expected_ca_sum = sum(range(1, 100, 2))
        actual_ca_sum = result.loc[result['state'] == 'CA', 'tot_death'].values[0]
        self.assertEqual(actual_ca_sum, expected_ca_sum)

    def test_by_state_image(self):
        """Tests if the deaths_by_state.png file is created."""
        graph_deaths_by_state(self.test_df)
        self.assertTrue(os.path.exists('deaths_by_state.png'), "deaths_by_state.png was not created")

    def test_oregon_freq_hist(self):
        """
        Tests the DataFrame returned by graph_oregon_death_freq.
        Verifies the binning logic (0, 1, 2, 5, 10...).
        """
        result = graph_oregon_death_freq(self.test_df)

        # Check DataFrame structure
        self.assertIsInstance(result, pd.DataFrame)
        self.assertListEqual(sorted(result.columns.tolist()), ['bin', 'tot_death'])

        # Check Bin Endpoints Logic
        # The prompt requires bins starting at 0, 1, 2, 5, 10, 20...
        expected_starts = [0, 1, 2, 5, 10]
        actual_starts = result['bin'].values

        # Verify the first few specific bins exist
        for val in expected_starts:
            self.assertIn(val, actual_starts)

        # Verify that after 10, bins increment by 10 (10, 20, 30...)
        bins_after_10 = [b for b in actual_starts if b >= 10]
        if len(bins_after_10) > 1:
            for i in range(len(bins_after_10) - 1):
                self.assertEqual(bins_after_10[i + 1] - bins_after_10[i], 10, "Bins after 10 should increment by 10")

    def test_oregon_freq_image(self):
        """Tests if the OR_death_freq.png file is created."""
        graph_oregon_death_freq(self.test_df)
        self.assertTrue(os.path.exists('OR_death_freq.png'), "OR_death_freq.png was not created")

    def test_over_time_image(self):
        """Tests if the deaths_over_time.png file is created."""
        graph_deaths_over_time(self.test_df)
        self.assertTrue(os.path.exists('deaths_over_time.png'), "deaths_over_time.png was not created")

    def test_over_time_totals(self):
        """
        Tests the DataFrame returned by graph_deaths_over_time.
        Verifies columns and that data was aggregated by date.
        """
        result = graph_deaths_over_time(self.test_df)

        # Check DataFrame structure
        self.assertIsInstance(result, pd.DataFrame)
        self.assertListEqual(sorted(result.columns.tolist()), ['submission_date', 'tot_death'])

        # Check that we have 100 rows (one for each date in our dummy data)
        self.assertEqual(len(result), 100)

        # Verify total sum is conserved
        # The sum of all 'tot_death' in result should equal sum of all 'new_death' in input
        self.assertEqual(result['tot_death'].sum(), self.test_df['new_death'].sum())


if __name__ == '__main__':
        unittest.main()