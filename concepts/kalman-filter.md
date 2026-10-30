---
title: Kalman filter
essence: "The exact Bayesian filter for linear-Gaussian models, carrying a mean and covariance through predict and update steps."
aliases: ["KF", "linear quadratic estimator", "LQE"]
domains: [estimation, control, probability]
status: seed
requires: ["[[gaussian-conditioning]]", "[[state-space-model]]"]
special_case_of: ["[[bayesian-filtering]]"]
analogous_to: ["[[linear-quadratic-regulator]]"]
contrasts_with: ["[[particle-filter]]"]
sources:
  - "Kalman, A New Approach to Linear Filtering and Prediction Problems (1960)"
  - "Särkkä & Svensson, Bayesian Filtering and Smoothing, 2nd ed. (2023)"
---

# Kalman filter

$$
\Large
x_t \mid y_{1:t} \sim \mathcal{N}(\underbrace{\hat x_{t\mid t}}_{\text{estimate}},\ \underbrace{P_{t\mid t}}_{\text{covariance}})
$$

## Definition
Model:
$$
x_t = A x_{t-1} + B u_{t-1} + w_{t-1}, \quad w \sim \mathcal{N}(0, Q); \qquad
y_t = C x_t + v_t, \quad v \sim \mathcal{N}(0, R).
$$
**Predict**
$$
\hat x_{t\mid t-1} = A \hat x_{t-1\mid t-1} + B u_{t-1}, \qquad
P_{t\mid t-1} = A P_{t-1\mid t-1} A^\top + Q.
$$
**Update**
$$
S_t = C P_{t\mid t-1} C^\top + R, \qquad K_t = P_{t\mid t-1} C^\top S_t^{-1},
$$
$$
\hat x_{t\mid t} = \hat x_{t\mid t-1} + K_t\,(y_t - C \hat x_{t\mid t-1}), \qquad
P_{t\mid t} = (I - K_t C)\, P_{t\mid t-1}.
$$

## Intuition
Track the hidden state of a linear system from noisy measurements by carrying a Gaussian belief. Push it through the dynamics (the mean moves, the uncertainty grows by $Q$), then blend in the measurement with a weight set by how uncertain the prediction is relative to the sensor. Because everything stays Gaussian, a mean and a covariance are the entire belief.

## Key results
- Exact Bayesian filter for this model: $p(x_t \mid y_{1:t}) = \mathcal{N}(\hat x_{t\mid t}, P_{t\mid t})$, so $\hat x_{t\mid t}$ is the MMSE estimate.
- Without the Gaussian assumption it is still the best *linear* estimator given only first and second moments.
- The covariance recursion is a Riccati difference equation that never touches $y_t$: gains can be precomputed. If $(A, C)$ is detectable and $(A, Q^{1/2})$ stabilisable, $P_{t\mid t-1}$ converges to the stabilising solution of the DARE (steady-state filter).
- Innovations $e_t = y_t - C\hat x_{t\mid t-1}$ are white with covariance $S_t$ under a correct model: the standard consistency check.
- Joseph form $P_{t\mid t} = (I - K_tC)P_{t\mid t-1}(I - K_tC)^\top + K_t R K_t^\top$ keeps $P$ symmetric positive definite numerically.

## Connections
- [[bayesian-filtering]] specialised to linear-Gaussian models; the update is the measurement form of [[gaussian-conditioning]].
- **Dual of the [[linear-quadratic-regulator]]**: the prior-covariance recursion is LQR's backward Riccati recursion under $A \mapsto A^\top$, $B \mapsto C^\top$, run forward in time, with noise covariances $Q, R$ in place of the cost weights. Hence the name "linear quadratic estimator". Symbol map in the LQR note.
- **Temporal [[gaussian-process]] regression**: GPs with Matérn-type kernels on a 1-D input have an equivalent linear state-space form, and the Kalman filter plus [[rts-smoother]] computes the GP posterior in $O(n)$ instead of $O(n^3)$.
- Versus the [[particle-filter]]: exact and cheap here, but limited to linear-Gaussian; particles handle arbitrary posteriors at a sampling cost. [[extended-kalman-filter]] sits in between.

## Open questions
