# Bayesian Theory Cheat Sheet for Computer Scientists

## 1. Introduction
- **Definition**: Uses probability to represent uncertainty, updates beliefs with Bayes' theorem.
- **Vs. Frequentist**: Parameters are random variables with priors, not fixed.

## 2. Core Concepts
- **Probability**: Degree of belief, not just frequency.
- **Prior**: Initial belief about parameters.
- **Likelihood**: Probability of data given parameters.
- **Posterior**: Updated belief after data.

## 3. Mathematical Foundations
- **Bayes' Theorem**:  
  \[
  P(\theta|D) = \frac{P(D|\theta)P(\theta)}{P(D)}
  \]
  - \(P(\theta)\): Prior
  - \(P(D|\theta)\): Likelihood
  - \(P(\theta|D)\): Posterior
  - \(P(D)\): Marginal likelihood
- **Conjugate Priors**: Prior and posterior in same family (e.g., Beta-Binomial).
- **Posterior Predictive**: Predict new data:  
  \[
  P(D_{\text{new}}|D) = \int P(D_{\text{new}}|\theta)P(\theta|D) \, d\theta
  \]

## 4. Bayesian Inference
- **Parameter Estimation**: Compute posterior for parameters.
- **Model Selection**: Use Bayes factors or posterior odds.
- **Predictive Distributions**: Forecast new data.

## 5. Bayesian Networks
- **Definition**: Graphical models with directed acyclic graph (DAG) for variable dependencies.
- **Structure**: Nodes (variables), edges (dependencies), conditional probability distributions (CPDs).
- **Joint Probability**:  
  \[
  P(X_1, \dots, X_n) = \prod_{i=1}^{n} P(X_i \mid \text{Parents}(X_i))
  \]
- **Inference**: Compute probabilities given evidence.
- **Learning**: Estimate CPDs and DAG structure.

## 6. Causal Networks
- **Definition**: Bayesian networks modeling causal relationships.
- **Structure**: DAG with causal edges.
- **Do-Calculus**: Rules for intervention effects.
- **Applications**: Healthcare, finance, marketing.

## 7. Advanced Topics
- **Markov Chain Monte Carlo (MCMC)**: Sampling for complex posteriors (e.g., Gibbs).
- **Variational Inference**: Approximates posteriors with simpler distributions.
- **Bayesian Deep Learning**: Uncertainty in neural networks.

## 8. Practical Tools
- **Software**: PyMC, Stan, Edward.
- **Bayesian Network Libraries**: pgmpy (Python](https://github.com/pgmpy/pgmpy), bnlearn (R).

## 9. Applications
- **Machine Learning**: Naive Bayes, Gaussian processes.
- **AI**: Probabilistic reasoning, expert systems.
- **Data Science**: Uncertainty quantification.

## 10. Motivations & Goals
- **Motivations**: Incorporates prior knowledge, handles uncertainty, updates beliefs.
- **Goals**: Parameter estimation, model selection, sequential experiment design, data structure exploration.