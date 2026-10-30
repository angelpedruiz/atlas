---
title: Notation
aliases: [house notation, conventions]
---

# Notation

House conventions for every concept note. Agents translate sources into this.
This is an initial proposal: change anything, and note the change in the commit.

## General

| object | notation | note |
|---|---|---|
| scalar, vector | $x \in \mathbb{R}^n$ | plain italic, no bold; dimension from context |
| matrix | $A, \Sigma$ | uppercase |
| transpose | $A^\top$ | not $A^T$ or $A'$ |
| positive (semi)definite | $A \succ 0$, $A \succeq 0$ | |
| identity | $I$ | |
| index sets | $y_{1:t} = (y_1,\dots,y_t)$ | |
| definition | $:=$ | |

## Probability

| object | notation | note |
|---|---|---|
| density / pmf | $p(x)$, $p(x \mid y)$ | one symbol for all densities |
| Gaussian | $\mathcal{N}(\mu, \Sigma)$, density $\mathcal{N}(x;\mu,\Sigma)$ | covariance, not std, as 2nd argument |
| expectation, covariance | $\mathbb{E}[\cdot]$, $\operatorname{Cov}[\cdot]$ | |
| precision | $\Lambda = \Sigma^{-1}$ | |
| joint blocks | $\Sigma_{ab}$ | block of $\operatorname{Cov}[(a,b)]$ |
| Gaussian process | $f \sim \mathcal{GP}(m, k)$ | |
| kernel, Gram matrix | $k(x,x')$, $K_{XX}$, $k_{*X}$ | Gram matrix always carries set subscripts |

## Dynamical systems, estimation, control

| object | notation | note |
|---|---|---|
| discrete time | $t \in \{0,1,\dots\}$ | $t$, not $k$ (frees $k$ for kernels) |
| state, input, measurement | $x_t$, $u_t$, $y_t$ | controls convention; ML's latent $z_t$ ↦ $x_t$, observation ↦ $y_t$ |
| linear model | $x_{t+1} = A x_t + B u_t + w_t$, $y_t = C x_t + v_t$ | $C$, not $H$ |
| noise covariances | $w_t \sim \mathcal{N}(0,Q)$, $v_t \sim \mathcal{N}(0,R)$ | |
| estimate given data to $s$ | $\hat x_{t\mid s}$, covariance $P_{t\mid s}$ | |
| Kalman gain | $K_t$ | always time-indexed |
| LQR weights | $Q \succeq 0$ (state), $R \succ 0$ (input) | deliberately the same letters as noise covariances: KF/LQR duality |
| LQR feedback gain | $u_t = -F_t x_t$ | $F$, to keep $K$ for the Kalman gain |
| Riccati / value matrix | $P_t$ | covariance in estimation, value matrix in control (duality again) |

## Decision making / RL

| object | notation | note |
|---|---|---|
| convention | **minimise cost** | control convention; RL reward $r = -\ell$ |
| stage cost, terminal cost | $\ell(x,u)$, $\ell_T(x)$ | |
| dynamics | $x' = f(x,u)$ or $x' \sim p(x' \mid x,u)$ | |
| discount | $\gamma \in [0,1)$ | |
| value, action-value | $V^\pi, V^*$, $Q^\pi, Q^*$ | $Q$-functions always carry a superscript, unlike the weight matrix $Q$ |
| policy | $\pi(u \mid x)$ or $u = \pi(x)$ | |
| transition matrix under $\pi$ | $\mathcal{P}_\pi$ | calligraphic, to avoid $P_t$ |
| Bellman operator | $\mathcal{T}$, $\mathcal{T}^\pi$ | |

## Known collisions

- $Q$: LQR state weight / process-noise covariance (intentional, dual) vs. $Q^\pi$ (always superscripted).
- $P$: estimation covariance / LQR value matrix (intentional, dual) vs. $\mathcal{P}_\pi$.
- $K$: Kalman gain $K_t$ (time index) vs. Gram matrix $K_{XX}$ (set index).
