# COVID-19 Data Visualization & Trend Analysis

This project implements a data visualization suite using **Matplotlib** and **Pandas** to analyze CDC COVID-19 death statistics. It transforms raw longitudinal data into professional-grade charts for state-level impact and time-series trends.

## 🚀 Features
- **Temporal Trend Mapping:** Visualizes daily reporting with 7-day, 30-day, and 90-day rolling averages to identify long-term pandemic trajectories.
- **Geographic Impact Analysis:** Aggregates and compares total mortality rates across all U.S. states and territories using dynamic bar charts.
- **Custom Frequency Profiling:** Implements a specialized histogram for Oregon data using a hybrid binning strategy (fixed small bins followed by decile increments).
- **Automated Export:** Programmatically generates and saves high-resolution `.png` visualizations (`deaths_by_state.png`, `deaths_over_time.png`, and `OR_death_freq.png`).
- **Data Integrity Logic:** Exclusively utilizes `new_death` metrics to calculate total mortality, ensuring alignment with automated execution test standards.

## 🛠️ Technical Implementation
- **Matplotlib Agg Backend:** Uses `matplotlib.use('Agg')` to facilitate automated execution and file saving without requiring a graphical user interface.
- **Rolling Window Engineering:** Leverages Pandas `rolling().mean()` to smooth erratic daily reporting data for clearer trend visualization.
- **Iterative Bin Generation:** Uses a dynamic `while` loop to construct histogram bins that scale based on the maximum reported values in the dataset.
- **Stable Data Structuring:** Returns summarized DataFrames with explicit type conversion (float) to maintain compatibility with verification utilities.

## 📊 Sample Usage
```python
import pandas as pd
from datavis import graph_deaths_by_state, graph_deaths_over_time, graph_oregon_death_freq

# Load raw CDC data
df = pd.read_csv('covid_state_data.csv')

# Note: Ensure submission_date is converted if not handled by the function
# df['submission_date'] = pd.to_datetime(df['submission_date'])

# Generate State-Level Summary Chart
state_df = graph_deaths_by_state(df)

# Generate Time-Series Scatter Plot with Moving Averages
time_df = graph_deaths_over_time(df)

# Generate Oregon-Specific Frequency Histogram
oregon_df = graph_oregon_death_freq(df)