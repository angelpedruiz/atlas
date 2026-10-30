---
title: Likelihood
essence: "How probable the observed data are under each hypothesis, read as a function of the hypothesis."
aliases: ["likelihood function"]
domains: [probability]
status: seed
requires: []
---

# Likelihood

## Intuition
Fix the data and ask how well each hypothesis predicted it. It scores hypotheses against each other, but it is not a probability of the hypothesis.

## Definition
For fixed data $y$, the function $\theta \mapsto p(y \mid \theta)$. It need not integrate to 1 over $\theta$.

## Connections
- The factor that reweights the prior in [[bayes-rule]].
- [[gaussian-process]] regression uses the Gaussian likelihood $y \mid f_X \sim \mathcal{N}(f_X, \sigma^2 I)$.
