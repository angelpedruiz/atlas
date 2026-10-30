---
title: Bellman equation
aliases: ["dynamic programming principle", "principle of optimality", "Bellman optimality equation"]
domains: [optimization, control, reinforcement-learning]
status: seed
requires: ["[[markov-decision-process]]"]
contrasts_with: ["[[pontryagin-minimum-principle]]"]
sources:
  - "Bellman, Dynamic Programming (1957)"
  - "Bertsekas, Dynamic Programming and Optimal Control, Vol. I"
  - "Sutton & Barto, Reinforcement Learning: An Introduction, 2nd ed. (2018), ch. 3–4"
---

# Bellman equation

## Intuition
The tail of an optimal plan is itself optimal from wherever it starts. So the value of a state is the best one-step cost plus the value of where you land, which turns a search over whole trajectories into a recursion over states.

## Definition
Cost-minimisation convention (see notation). Finite horizon, deterministic:
$$
V_t(x) = \min_u \big[ \ell(x, u) + V_{t+1}(f(x, u)) \big], \qquad V_T = \ell_T .
$$
Infinite horizon, discounted, stochastic:
$$
V^*(x) = \min_u \Big\{ \ell(x, u) + \gamma\, \mathbb{E}\big[ V^*(x') \mid x, u \big] \Big\}, \qquad \gamma \in [0, 1),
$$
$$
Q^*(x, u) = \ell(x, u) + \gamma\, \mathbb{E}\Big[ \min_{u'} Q^*(x', u') \;\Big|\; x, u \Big].
$$
RL form: $r = -\ell$ and $\min \to \max$.

## Key results
- The Bellman operator $\mathcal{T}$ is a $\gamma$-contraction in $\lVert\cdot\rVert_\infty$: unique fixed point $V^*$, and value iteration converges geometrically (Banach).
- Policy evaluation is linear: $V^\pi = \ell_\pi + \gamma \mathcal{P}_\pi V^\pi \Rightarrow V^\pi = (I - \gamma \mathcal{P}_\pi)^{-1}\ell_\pi$.
- Value iteration, policy iteration and [[q-learning]] are all ways to find or approximate the fixed point.
- Continuous-time limit: the [[hamilton-jacobi-bellman-equation]], $-\partial_t V = \min_u \{ \ell(x, u) + \nabla_x V^\top f(x, u) \}$.

## Connections
- [[linear-quadratic-regulator]]: the special case with a closed-form solution (quadratic $V$).
- Same chain-DP structure as [[bayesian-filtering]], in the $(\min, +)$ semiring instead of $(\int, \times)$ and run backward instead of forward.
- Versus [[pontryagin-minimum-principle]]: DP gives a global feedback law over all states but suffers the curse of dimensionality; Pontryagin gives necessary conditions along one trajectory (open-loop) and scales to large state spaces.

## Open questions
