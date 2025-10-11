---
tags: [optimization, reference, guide]
---

# Optimization and Constraint Satisfaction Cheat Sheet for Computer Scientists

## Introduction
Optimization finds the best solution by minimizing/maximizing an objective function. Constraint satisfaction finds solutions meeting all constraints. Both are key in AI, operations research, and algorithm design.

## Constraint Satisfaction Problems (CSPs)
- **Definition**: A CSP is a triple \(\langle X, D, C \rangle\):
  - \(X = \{X_1, \ldots, X_n\}\): Variables.
  - \(D = \{D_1, \ldots, D_n\}\): Domains of possible values.
  - \(C = \{C_1, \ldots, C_m\}\): Constraints on variable combinations.
- **Solving Methods**:
  - **Backtracking**: Systematic search, assigns values, backtracks on conflicts.
  - **Constraint Propagation**: Reduces domains (e.g., arc consistency).
  - **Local Search**: Iteratively improves complete assignments.
- **Applications**:
  - Scheduling (e.g., timetabling).
  - Planning (e.g., robot paths).
  - Configuration (e.g., hardware setup).
  - Resource allocation.

## Constrained Optimization
- **Definition**: Optimize \(f(\mathbf{x})\) subject to:
  - Equality constraints: \(g_i(\mathbf{x}) = c_i\).
  - Inequality constraints: \(h_j(\mathbf{x}) \geq d_j\).
- **Types of Constraints**:
  - Hard: Must be satisfied.
  - Soft: Penalized if violated.
- **Solution Methods**:
  - Substitution: Substitute constraints into objective.
  - Lagrange Multipliers: For equality constraints.
  - KKT Conditions: For inequality constraints.
  - Linear/Nonlinear/Quadratic Programming.
- **Applications**:
  - Resource allocation (e.g., bandwidth).
  - Machine learning (e.g., SVM optimization).
  - Logistics (e.g., routing).

## Relationship
Constrained optimization extends CSPs by adding an objective function. CSP techniques can solve optimization by iteratively tightening objective constraints.

## Advanced Topics
- **Complexity**: CSPs and optimization often NP-complete; some subclasses tractable (e.g., bounded treewidth).
- **Heuristics**: Guide search (e.g., min-conflicts).
- **Approximation**: For infeasible exact solutions.

## Tools
- OR-Tools (Google).
- CPLEX, Gurobi (commercial).
- JaCoP, Minion (open-source).

## References
- [Constraint Satisfaction Problem](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem)
- [Constrained Optimization](https://en.wikipedia.org/wiki/Constrained_optimization)
- [OR-Tools](https://developers.google.com/optimization/cp)
- [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0377221798003646)