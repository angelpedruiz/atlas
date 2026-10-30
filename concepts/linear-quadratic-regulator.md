---
title: Linear-quadratic regulator
aliases: ["LQR"]
domains: [control, optimization]
status: seed
requires: ["[[riccati-equation]]", "[[state-space-model]]"]
special_case_of: ["[[bellman-equation]]"]
sources:
  - "Anderson & Moore, Optimal Control: Linear Quadratic Methods (1990)"
  - "Bertsekas, Dynamic Programming and Optimal Control, Vol. I"
  - "Fazel, Ge, Kakade & Mesbahi, Global Convergence of Policy Gradient Methods for the Linear Quadratic Regulator (2018)"
---

# Linear-quadratic regulator

## Intuition
For a linear system penalised quadratically on state deviation and control effort, the optimal policy is a fixed linear feedback. $Q$ versus $R$ trades how fast you converge against how hard you push. Everything is solvable because a quadratic value function stays quadratic under the Bellman backup.

## Definition
Finite horizon, discrete time:
$$
x_{t+1} = A x_t + B u_t, \qquad
J = x_T^\top Q_f x_T + \sum_{t=0}^{T-1} \big( x_t^\top Q x_t + u_t^\top R u_t \big), \qquad Q \succeq 0,\ R \succ 0.
$$
The optimal policy is $u_t = -F_t x_t$ with
$$
F_t = (R + B^\top P_{t+1} B)^{-1} B^\top P_{t+1} A,
$$
$$
P_t = Q + A^\top P_{t+1} A - A^\top P_{t+1} B (R + B^\top P_{t+1} B)^{-1} B^\top P_{t+1} A, \qquad P_T = Q_f,
$$
and optimal cost-to-go $V_t(x) = x^\top P_t x$.

## Key results
- **Derivation.** Assume $V_{t+1}(x) = x^\top P_{t+1} x$, substitute into the Bellman equation, minimise the resulting quadratic in $u$: the minimiser is linear in $x$ and $V_t$ is again quadratic. Induction closes.
- **Infinite horizon.** If $(A, B)$ is stabilisable and $(A, Q^{1/2})$ detectable, $P_t \to P$, the stabilising solution of the DARE, and $A - BF$ is Schur stable.
- **Certainty equivalence.** Additive Gaussian process noise leaves $F$ unchanged (only adds a constant to the cost). With noisy partial observations, the optimal controller is a Kalman filter feeding LQR, designed separately: [[linear-quadratic-gaussian]].
- **Continuous time.** $A^\top P + PA - PBR^{-1}B^\top P + Q = 0$, $u = -R^{-1}B^\top P x$.

## Connections
- The rare case where the [[bellman-equation]] is solved exactly in closed form.
- **Dual of the [[kalman-filter]]** (edge declared there):

| LQR (backward) | KF (forward) |
|---|---|
| $A$ | $A^\top$ |
| $B$ | $C^\top$ |
| state weight $Q$ | process-noise covariance $Q$ |
| input weight $R$ | measurement-noise covariance $R$ |
| value matrix $P_t$ | prior covariance $P_{t\mid t-1}$ |
| gain $F_t$ | $(A K_t)^\top$, the one-step-predictor gain |

- Standard testbed for model-free RL: policy gradient on the (non-convex) LQR cost still converges globally (Fazel et al. 2018).

## Open questions
