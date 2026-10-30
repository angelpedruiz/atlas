---
title: KL divergence
essence: "How far a distribution q is from a reference p, measured as the expected log ratio of their densities under q."
aliases: ["Kullback-Leibler divergence", "relative entropy"]
domains: [probability]
status: seed
requires: []
sources:
  - "Cover & Thomas, Elements of Information Theory, 2nd ed. (2006), ch. 2"
---

# KL divergence

**Definition.** For distributions $q$ and $p$ on the same space, the *KL divergence* from $p$ to $q$ is
$$
\Large
\operatorname{KL}(q \,\Vert\, p) := \mathbb{E}_{x \sim q}\Big[\underbrace{\log \frac{q(x)}{p(x)}}_{\text{log ratio}}\Big]
$$
It is non-negative, zero only when $q = p$, and not symmetric.

## Intuition
Sample from $q$ and ask how much more likely each sample is under $q$ than under $p$. It behaves like a distance but isn't one: swapping the arguments asks a different question.

## Connections
- [[variational-inference]] minimises $\operatorname{KL}(q \,\Vert\, p(\theta \mid y))$ over a tractable family.
- Maximising the [[likelihood]] on many samples minimises the KL divergence from the model to the data distribution.
