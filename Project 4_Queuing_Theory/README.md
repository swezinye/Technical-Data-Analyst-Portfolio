# Queuing System Optimizer
### A Pythonic Implementation of M/M/c and Priority Queuing Models

# Advanced Queuing Theory & Little's Law System

This project is an advanced implementation of M/M/c queuing models, featuring multi-class priority service logic and an automated metrics engine based on Little's Law.

## 🚀 Key Features
- **Priority Queue Analysis**: Implements $B_k$ (blocking probability components) to calculate waiting times for specific service classes (e.g., Gold vs. Silver members).
- **Little's Law Engine**: A "universal" function that takes any one system metric ($L, L_q, W, W_q$) and automatically derives all others using steady-state relationships.
- **Strict Validation**: Unified parameter checking for arrival rates ($\lambda$), service rates ($\mu$), and server counts ($c$).

## 🧮 Advanced Formulas
- **Priority Wait Time ($W_{q,k}$):** $$W_{q,k} = \frac{(1-\rho)W_q}{B_{k-1}B_k}$$
- **Little's Law Relationships:** - $L = \lambda W$
  - $L_q = \lambda W_q$
  - $W = W_q + \frac{1}{\mu}$

## 🧪 Testing
The library includes a comprehensive `unittest` suite covering:
- Scalar and Tuple/List arrival rates.
- System feasibility boundaries ($\rho \to 1$).
- Individual priority class performance metrics.