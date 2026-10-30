---
title: Gaussian process
essence: "A distribution over functions whose values at any finite set of inputs are jointly Gaussian, with covariance given by a kernel."
aliases: ["GP", "Gaussian process regression", "GPR", "kriging"]
domains: [machine-learning, probability]
status: seed
requires: ["[[gaussian-conditioning]]", "[[kernel-function]]"]
equivalent_to: ["[[kernel-ridge-regression]]"]
analogous_to: ["[[kalman-filter]]"]
sources:
  - "ETH Zurich, Probabilistic Artificial Intelligence, lecture 3"
  - "Rasmussen & Williams, Gaussian Processes for Machine Learning (2006), ch. 2"
  - "Hartikainen & Särkkä, Kalman filtering and smoothing solutions to temporal Gaussian process regression models (2010)"
---

# Gaussian process

**Definition.** A family of random variables $\{f(x) : x \in \mathcal{X}\}$ is a *Gaussian process* if every finite collection is jointly Gaussian. We write
$$
\Large
f \sim \mathcal{GP}(\underbrace{\mu}_{\text{mean function}},\ \underbrace{k}_{\text{kernel}})
$$
with $\mu(x) = \mathbb{E}[f(x)]$ and $k(x, x') = \operatorname{Cov}(f(x), f(x'))$. For any finite $A = \{x_1, \dots, x_m\}$,
$$
f_A \sim \mathcal{N}(\mu_A, K_{AA}).
$$

**Posterior.** Observe $y_i = f(x_i) + \varepsilon_i$ with $\varepsilon_i \sim \mathcal{N}(0, \sigma_n^2)$, and let $K_y = K_{AA} + \sigma_n^2 I$. By [[gaussian-conditioning]], $f \mid \mathcal{D} \sim \mathcal{GP}(\mu_D, k_D)$ with
$$
\begin{cases}
\mu_D(x) = \mu(x) + k_{xA} K_y^{-1} (y_A - \mu_A) \\
k_D(x, x') = k(x, x') - k_{xA} K_y^{-1} k_{Ax'}
\end{cases}
$$

## Intuition
A prior over functions, specified only by how their values co-vary: the kernel says similar inputs have similar outputs. Learning from data is just conditioning a big Gaussian.
