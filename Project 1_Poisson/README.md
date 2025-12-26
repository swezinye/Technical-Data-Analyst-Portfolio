# Poisson Distribution Calculator

A Python-based implementation of Poisson distribution functions, including Probability Mass Function (PMF), Cumulative Distribution Function (CDF), and Inverse Cumulative Distribution (Quantile) function.

## 📊 Project Overview
This project was developed to implement the logic for calculating Poisson probabilities from scratch, without relying on high-level statistical libraries like `scipy`. It focuses on:
- **Recursive Logic:** Implementing factorials using recursion with depth limits.
- **Statistical Accuracy:** Handling PMF and CDF calculations based on the rate parameter ($\lambda$).
- **Robust Error Handling:** Strict adherence to mathematical domains (handling non-integers, negative values, and infinity).

## 🛠️ Functions Included
The library (`pois.py`) follows the naming conventions used in the R programming language:

- `factorial(x)`: Calculates $x!$ using recursion (capped at 1,000 to prevent stack overflow).
- `dpois(x, lamda)`: Calculates the **Probability Mass Function** $P(X = x)$.
- `ppois(x, lamda)`: Calculates the **Cumulative Probability** $P(X \leq x)$.
- `qpois(alpha, lamda)`: Calculates the **Inverse Cumulative Probability** (finds the smallest $x$ such that $P(X \leq x) \geq \alpha$).

## 🧪 Testing
The project includes a comprehensive test suite (`pois_tests.py`) that verifies:
1. **Standard Cases:** Valid integer inputs and expected probability outcomes.
2. **Edge Cases:** $x=0$, $\lambda=0$, and very large/small probabilities.
3. **Error Cases:** Handling of negative numbers, non-integers, and out-of-bounds $\alpha$ values (returns `math.nan` or `inf` as specified).

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Poisson_Project.git](https://github.com/YOUR_USERNAME/Poisson_Project.git)