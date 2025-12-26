# Simple Least Squares Regression (LSR) Calculator

A robust Python implementation of Simple Linear Regression that calculates regression coefficients ($\beta_0$ and $\beta_1$) using two distinct programming paradigms.

## 📊 Project Overview
This project was developed to demonstrate mastery of both foundational algorithmic logic and advanced "Pythonic" features. It calculates the line of best fit for a given set of independent ($x$) and dependent ($y$) variables.

The core goal is to solve:
$$\hat{y}_i = \beta_0 + \beta_1 x_i$$

## 🛠 Features
### 1. Dual Implementation
- **Manual Iteration (`regress`)**: Uses explicit `while` loops and manual accumulators. It avoids all high-level Python abstractions (no `sum()`, `len()`, or comprehensions) to showcase low-level data processing skills.
- **Pythonic Implementation (`regress_comp`)**: Utilizes List Comprehensions and built-in aggregation functions for cleaner, more efficient code.

### 2. Comprehensive Data Validation
The functions are designed with strict error handling, returning specific codes for data integrity issues:
- `-1`: Length Mismatch between $x$ and $y$.
- `-2 / -3`: Input is not an Iterable.
- `-4`: Non-numeric data, `NaN` values, empty inputs, or an undefined slope ($S_{xx} = 0$).

### 3. Automated Testing Suite
Includes a professional-grade `pytest` suite that:
- Validates mathematical accuracy against known datasets.
- Tests all edge cases and error codes.
- Features a **CSV Data Loader** to run regressions on external files (`regress_data.csv`).

## 🚀 How to Run
### Prerequisites
Ensure you have `pytest` and `toolz` installed:
```bash
pip install pytest toolz