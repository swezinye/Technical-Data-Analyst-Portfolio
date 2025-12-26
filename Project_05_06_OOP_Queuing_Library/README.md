# Object-Oriented Queuing Theory Library

A modular Python library for calculating performance metrics across various queuing models (M/M/1, M/M/c, M/D/1, M/G/1, and Priority Systems).

## 🏗 System Architecture
This library utilizes an **Object-Oriented Hierarchy** to minimize code duplication and maximize mathematical integrity. 

- **BaseQueue (Abstract):** Implements universal performance metrics (Little's Law) and handles state management using a "Dirty Flag" pattern (`_recalc_needed`).
- **Inheritance:** Specialized queue types inherit from the base and implement specific probability mass and density logic.
- **State Integrity:** All setters perform real-time validation, ensuring the system remains in a mathematically valid state.

## 🧮 Theoretical Models Implemented
- **M/M/1**: Poisson arrivals with Exponential service.
- **M/M/c**: Multi-server systems using the Erlang-C distribution.
- **M/D/1**: Constant service time models.
- **M/G/1**: General service distributions using the Pollaczek–Khinchine formula.
- **M/M/c/Priority**: Non-preemptive priority classes with wait-time derivations for each tier.

## 🧪 Robust Testing
The library includes a comprehensive `unittest` and `pytest` suite that verifies:
- Mathematical convergence with theoretical expected values.
- Proper handling of infeasible systems ($\rho \ge 1$).
- Validity of inputs (NaN propagation).