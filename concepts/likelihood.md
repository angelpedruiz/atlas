---
title: Likelihood
essence: "How probable the observed data are under each parameter value, read as a function of the parameter."
aliases: ["likelihood function"]
domains: [probability]
status: seed
requires: []
---

# Likelihood

$$
\Large
p(\underbrace{y}_{\text{observation}} \mid \underbrace{\theta}_{\text{parameter}})
$$

## Intuition
Fix the data and ask how well each parameter value predicted it. It scores parameter values against each other, but it is not a probability of the parameter.

## Definition
The function $\theta \mapsto p(y \mid \theta)$ for fixed data $y$. It need not integrate to 1 over $\theta$.

## Connections
- The factor that reweights the prior in [[bayes-rule]].
- [[gaussian-process]] regression uses the Gaussian likelihood $y \mid f_X \sim \mathcal{N}(f_X, \sigma^2 I)$.
