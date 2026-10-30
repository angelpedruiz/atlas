---
title: Kernel ridge regression
essence: "Regularised least squares over a kernel-defined function space, whose solution is a weighted sum of kernels centred on the training inputs."
aliases: ["KRR"]
domains: [machine-learning]
status: seed
requires: ["[[kernel-function]]", "[[linear-regression]]"]
sources:
  - "Rasmussen & Williams, Gaussian Processes for Machine Learning (2006), ch. 6"
---

# Kernel ridge regression

$$
\Large
\hat f(x_*) = \underbrace{k_{*X}}_{\text{similarity to data}}\ \underbrace{(K_{XX} + \lambda I)^{-1} y}_{\text{weights}}
$$

## Definition
$$
\hat f = \arg\min_{f \in \mathcal{H}_k} \sum_{i=1}^n (y_i - f(x_i))^2 + \lambda \lVert f \rVert_{\mathcal{H}_k}^2 .
$$

## Intuition
Fit a function to data while paying for its complexity, where the kernel decides what complex means. Even though the search runs over a possibly infinite-dimensional function space, the answer only ever needs one weight per training point, so the problem reduces to a linear solve.

## Key results
- Representer theorem: $\hat f(x_*) = \sum_{i=1}^n \alpha_i\, k(x_*, x_i)$ with $\alpha = (K_{XX} + \lambda I)^{-1} y$, so $\hat f(x_*) = k_{*X}(K_{XX} + \lambda I)^{-1} y$.
- Fitting costs $O(n^3)$ in the number of data points, whatever the dimension of the feature space.
- A linear kernel recovers ordinary ridge regression.

## Connections
- **Equivalent to the posterior mean of a [[gaussian-process]]**; the symbol map and scope are in that note.
- **MAP reading via [[bayes-rule]]**: with a zero-mean GP prior and Gaussian noise, the objective is the negative log posterior up to scale, with $\lambda = \sigma^2$.

## Open questions
