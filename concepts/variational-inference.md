---
title: Variational inference
essence: "Approximate an intractable posterior by the closest member of a tractable family, turning integration into optimisation."
aliases: ["VI", "variational Bayes"]
domains: [probability, machine-learning]
status: seed
requires: ["[[bayes-rule]]"]
sources:
  - "Blei, Kucukelbir & McAuliffe, Variational Inference: A Review for Statisticians (2017)"
---

# Variational inference

**Definition.** When the posterior in [[bayes-rule]] is intractable, *variational inference* approximates it by the closest member of a tractable family $\mathcal{Q}$:
$$
\Large
q^* = \operatorname*{argmin}_{q \in \mathcal{Q}} \underbrace{\operatorname{KL}\big(q(\theta) \,\Vert\, p(\theta \mid y)\big)}_{\text{mismatch to the posterior}}
$$
Equivalently, it maximises the evidence lower bound, built from the [[likelihood]]:
$$
\log p(y) \ge \mathbb{E}_q[\log p(y \mid \theta)] - \operatorname{KL}\big(q(\theta) \,\Vert\, p(\theta)\big).
$$

## Intuition
If the exact posterior can't be computed, pick a family of distributions you can work with and find the member closest to it. The hard integral becomes an optimisation problem.
