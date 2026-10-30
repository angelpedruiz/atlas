---
title: Bayesian filtering
essence: "Keep a belief over a hidden state by alternating a prediction through the dynamics with a Bayes update from each measurement."
aliases: ["recursive Bayesian estimation", "Bayes filter", "sequential Bayesian inference"]
domains: [probability, estimation]
status: seed
requires: ["[[bayes-rule]]", "[[state-space-model]]"]
analogous_to: ["[[bellman-equation]]"]
sources:
  - "Särkkä & Svensson, Bayesian Filtering and Smoothing, 2nd ed. (2023)"
---

# Bayesian filtering

$$
\Large
p(\underbrace{x_t}_{\text{hidden state}} \mid \underbrace{y_{1:t}}_{\text{measurements so far}})
$$

## Definition
Markov state-space model: $x_t \sim p(x_t \mid x_{t-1})$, $y_t \sim p(y_t \mid x_t)$, with $y_t$ conditionally independent of everything else given $x_t$. The filtering distribution $p(x_t \mid y_{1:t})$ obeys

**Predict** (Chapman–Kolmogorov)
$$
p(x_t \mid y_{1:t-1}) = \int p(x_t \mid x_{t-1})\, p(x_{t-1} \mid y_{1:t-1})\, dx_{t-1}
$$
**Update** (Bayes)
$$
p(x_t \mid y_{1:t}) = \frac{p(y_t \mid x_t)\, p(x_t \mid y_{1:t-1})}{p(y_t \mid y_{1:t-1})}.
$$

## Intuition
A hidden state evolves and we see noisy glimpses of it. Keep a belief over the state and alternate two moves: let the belief drift and spread according to the dynamics, then sharpen it with Bayes' rule when a measurement arrives. The belief at time $t$ summarises all past data, so nothing else needs to be stored.

## Key results
- Closed form only in special cases: linear-Gaussian gives the [[kalman-filter]]; a finite state space gives the forward algorithm of the [[hidden-markov-model]]. Otherwise approximate: [[extended-kalman-filter]], [[particle-filter]].
- **Prediction-error decomposition.** The normalisers multiply to the marginal likelihood, which is how model parameters are fitted:
  $$
  p(y_{1:T}) = \prod_{t} p(y_t \mid y_{1:t-1}).
  $$
- Smoothing $p(x_t \mid y_{1:T})$ needs an extra backward pass ([[rts-smoother]] in the linear-Gaussian case).

## Connections
- **Analogous to the [[bellman-equation]].** Both are dynamic programming on a chain. Filtering runs forward and *integrates out* the past, using $(\textstyle\int, \times)$; Bellman runs backward and *optimises out* the future, using $(\min, +)$. Replacing the integral by a max in filtering gives the [[viterbi-algorithm]], which in negative-log space is literally a min-sum Bellman recursion.
- Each update step is a single application of [[bayes-rule]].

## Open questions
