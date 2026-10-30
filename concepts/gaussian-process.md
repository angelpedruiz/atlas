---
title: Gaussian process
aliases: ["GP", "Gaussian process regression", "GPR", "kriging"]
domains: [machine-learning, probability]
status: seed
requires: ["[[gaussian-conditioning]]", "[[kernel-function]]"]
equivalent_to: ["[[kernel-ridge-regression]]"]
analogous_to: ["[[kalman-filter]]"]
sources:
  - "Rasmussen & Williams, Gaussian Processes for Machine Learning (2006), ch. 2"
  - "Hartikainen & Särkkä, Kalman filtering and smoothing solutions to temporal Gaussian process regression models (2010)"
---

# Gaussian process

## Intuition
A prior over functions specified only by how function values co-vary: the kernel says "inputs that are similar have similar outputs". Any finite set of function values is jointly Gaussian, so learning from data is just conditioning a big Gaussian, and the posterior comes with calibrated error bars for free.

## Definition
$f \sim \mathcal{GP}(m, k)$ iff for every finite $X = \{x_1, \dots, x_n\}$, $f_X \sim \mathcal{N}(m_X, K_{XX})$ with $[K_{XX}]_{ij} = k(x_i, x_j)$.

**Regression.** With $y = f_X + \varepsilon$, $\varepsilon \sim \mathcal{N}(0, \sigma^2 I)$ and $k_{*X} = [k(x_*, x_1), \dots, k(x_*, x_n)]$:
$$
\mu_*(x_*) = m(x_*) + k_{*X}(K_{XX} + \sigma^2 I)^{-1}(y - m_X),
$$
$$
\sigma_*^2(x_*) = k(x_*, x_*) - k_{*X}(K_{XX} + \sigma^2 I)^{-1} k_{X*}.
$$

## Key results
- The posterior is [[gaussian-conditioning]] with $a = f(x_*)$, $b = y$, $\Sigma_{ab} = k_{*X}$, $\Sigma_{bb} = K_{XX} + \sigma^2 I$. In particular $\sigma_*^2$ does not depend on $y$.
- Exact inference costs $O(n^3)$ (Cholesky of $K_{XX} + \sigma^2 I$).
- Hyperparameters $\theta$ are fitted by maximising the [[marginal-likelihood]], with $K_y = K_{XX} + \sigma^2 I$:
$$
\log p(y \mid X, \theta) = -\tfrac12 (y - m_X)^\top K_y^{-1}(y - m_X) - \tfrac12 \log\det K_y - \tfrac{n}{2}\log 2\pi .
$$

## Connections
- **Equivalent to [[kernel-ridge-regression]] for the posterior mean.** KRR solves $\min_{f \in \mathcal{H}_k} \sum_i (y_i - f(x_i))^2 + \lambda \lVert f \rVert_{\mathcal{H}_k}^2$, giving $\hat f(x_*) = k_{*X}(K_{XX} + \lambda I)^{-1} y$. With $m = 0$ and $\lambda = \sigma^2$ this is $\mu_*$. Scope: the mean only; the GP adds $\sigma_*^2$, KRR adds the regularisation reading.
- *Kriging* (geostatistics) is the same object under another name, kept as an alias.
- **Analogous to the [[kalman-filter]]**: for 1-D inputs and Matérn-type kernels the GP is the output of a linear SDE, and Kalman filtering + smoothing gives the same posterior in $O(n)$.
- The surrogate model in [[bayesian-optimization]].

## Open questions
