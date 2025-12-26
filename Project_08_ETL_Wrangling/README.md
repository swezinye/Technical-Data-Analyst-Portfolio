# Python Data Wrangling & ETL Toolkit

This project demonstrates advanced data engineering capabilities, focusing on the ETL (Extract, Transform, Load) lifecycle. It utilizes Python and Pandas to clean, consolidate, and restructure complex datasets for analytical readiness.

## 🛠️ Key Functionalities

### 1. Multi-File Consolidation (`combineSamples`)
- **Action**: Programmatically searches for and merges multiple CSV files using Unix-style pattern matching (e.g., `boiler_sample_*.csv`).
- **Feature**: Automatically performs a 60/40 split into **Control** and **Test** groups to prepare data for machine learning or quality assurance.

### 2. Data Reshaping (`reformatSamples`)
- **Action**: Transforms "Long" format observational data into "Wide" format sample rows.
- **Feature**: Dynamically generates headers (e.g., `obs.1`, `obs.2`) while verifying that all samples contain a uniform number of observations.



### 3. Regex Coordinate Extraction (`extractCoordinates`)
- **Action**: Uses Regular Expressions (Regex) to parse geographical metadata from complex string fields (e.g., `(14.63, -90.50)`).
- **Feature**: Converts string data into numeric `lat` and `lon` columns while providing case-insensitive validation for required headers.



### 4. Text Characterization (`analyzeWords`)
- **Action**: Generates a statistical profile of a word series.
- **Feature**: Calculates alphabetical distributions, word-length frequencies, and identifies specific string patterns using advanced pattern matching.

## 📊 Sample Output
The toolkit returns structured dictionaries and Pandas DataFrames. For example, the `analyzeWords` function produces:
- **letter_counts**: A dictionary mapping 'a-z' to frequency.
- **oo_words**: A subset of words containing "oo" patterns.
- **size_counts**: A distribution of word lengths found in the dataset.

## 🧪 Testing
The project includes a robust test suite (`test_project8.py`) to ensure:
- Data type integrity (Series vs. Lists).
- Error code propagation (e.g., -1 or -2 for missing columns).
- Correct handling of uneven or empty data samples.