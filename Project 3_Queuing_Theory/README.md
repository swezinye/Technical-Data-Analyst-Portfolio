# M/M/c Queuing Theory Calculator

A Python library for calculating steady-state performance metrics for single-server (M/M/1) and multi-server (M/M/c) queuing systems, including priority classes.

## 📈 Project Overview
This project models systems where customers arrive according to a Poisson process and are served at an exponential rate. It provides functions to validate system parameters, check for system stability (feasibility), and calculate key metrics such as:
- **P0**: The probability that the system is empty.
- **Lq**: The average number of customers waiting in the queue.

## 🛠 Features
- **Priority Class Support**: Automatically aggregates arrival rates ($\lambda$) from tuples or lists for priority queue modeling.
- **Mathematical Accuracy**: Implements the M/M/c summation formula and Little's Law relationships.
- **Robust Error Handling**: Handles infeasible systems (utilization $\rho \geq 1$) by returning `math.inf` and invalid inputs by returning `math.nan`.

## 🧮 Formulas
- **Utilization ($\rho$):** $$\rho = \frac{\lambda}{c\mu}$$
- **M/M/1 Lq:** $$L_q = \frac{\rho^2}{1-\rho}$$
- **M/M/c P0:** $$P_0 = \left[ \sum_{n=0}^{c-1} \frac{({\lambda/\mu})^n}{n!} + \frac{({\lambda/\mu})^c}{c!(1-\rho)} \right]^{-1}$$

## 🚀 How to Run
```bash
python queues_tests.py