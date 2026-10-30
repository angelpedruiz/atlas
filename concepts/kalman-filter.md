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

**Definition.** For a linear-Gaussian [[state-space-model]]
$$
\begin{cases}
x_t = A x_{t-1} + B u_{t-1} + w_{t-1}, & w \sim \mathcal{N}(0, Q) \\
y_t = C x_t + v_t, & v \sim \mathcal{N}(0, R)
\end{cases}
$$
the *Kalman filter* is the exact [[bayesian-filtering|Bayesian filter]]. It tracks the belief
$$
\Large
x_t \mid y_{1:t} \sim \mathcal{N}(\underbrace{\hat x_{t\mid t}}_{\text{estimate}},\ \underbrace{P_{t\mid t}}_{\text{covariance}})
$$
by alternating two steps.

**Predict**
$$
\begin{cases}
\hat x_{t\mid t-1} = A \hat x_{t-1\mid t-1} + B u_{t-1} \\
P_{t\mid t-1} = A P_{t-1\mid t-1} A^\top + Q
\end{cases}
$$
**Update**, by [[gaussian-conditioning]]
$$
\begin{cases}
S_t := C P_{t\mid t-1} C^\top + R \\
K_t := P_{t\mid t-1} C^\top S_t^{-1} \\
\hat x_{t\mid t} = \hat x_{t\mid t-1} + K_t\,(y_t - C \hat x_{t\mid t-1}) \\
P_{t\mid t} = (I - K_t C)\, P_{t\mid t-1}
\end{cases}
$$

## Intuition
Carry a Gaussian belief over the hidden state. Push it through the dynamics, then blend in the measurement, weighted by how uncertain the prediction is relative to the sensor.
