---
title: Bayes' rule
essence: "The posterior is the prior reweighted by how well each hypothesis explains the data, then renormalised."
aliases: ["Bayes' theorem", "Bayes theorem", "inverse probability"]
domains: [probability]
status: seed
requires: []
sources:
  - "Bishop, Pattern Recognition and Machine Learning (2006), §1.2"
---

# Bayes' rule

$$
\Large
\underbrace{p(\theta \mid y)}_{\text{posterior}} = \frac{\overbrace{p(y \mid \theta)}^{\text{likelihood}}\; \overbrace{p(\theta)}^{\text{prior}}}{\underbrace{p(y)}_{\text{evidence}}}
$$

## Definition
For random variables $\theta$ and $y$ with densities,
$$
p(\theta \mid y) = \frac{p(y \mid \theta)\, p(\theta)}{p(y)}, \qquad p(y) = \int p(y \mid \theta)\, p(\theta)\, d\theta .
$$
Prior $p(\theta)$; [[likelihood]] $p(y \mid \theta)$ read as a function of $\theta$; evidence (marginal likelihood) $p(y)$; posterior $p(\theta \mid y)$.

## Intuition
We usually know how data arise from a hypothesis, but want the reverse: how plausible each hypothesis is given the data. The posterior is the prior reweighted by how well each hypothesis explains what was observed, then renormalised.

## Key results
- **Sequential updating.** If $y_1 \perp y_2 \mid \theta$, yesterday's posterior is today's prior:
  $$
  p(\theta \mid y_{1:2}) \propto p(y_2 \mid \theta)\, p(\theta \mid y_1).
  $$
- **Conjugacy.** When prior and likelihood come from matching families the posterior stays in the family, and the update is a parameter map instead of an integral.
- **The evidence** does not affect the posterior's shape, but it is the quantity used to compare models and fit hyperparameters ([[marginal-likelihood]]).

## Connections
- Sequential updating with a moving state is [[bayesian-filtering]]: Bayes' rule alternated with a prediction step.
- The Gaussian–linear conjugate pair is [[gaussian-conditioning]], which is where most closed-form Bayesian computations in estimation and GPs come from.
- When $p(y)$ is intractable, the posterior is approximated instead, e.g. by [[variational-inference]].

