---
title: Gaussian conditioning
essence: "Conditioning on part of a jointly Gaussian vector gives a Gaussian whose mean shifts linearly with the observation and whose covariance shrinks by an amount independent of it."
aliases: ["conditional Gaussian", "conditioning a joint Gaussian"]
domains: [probability, linear-algebra]
status: seed
requires: ["[[multivariate-gaussian]]", "[[schur-complement]]"]
sources:
  - "Bishop, Pattern Recognition and Machine Learning (2006), §2.3.1–2.3.3"
---

# Gaussian conditioning

$$
a \mid b \sim \mathcal{N}\big(\underbrace{\mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(b - \mu_b)}_{\text{shifted mean}},\ \underbrace{\Sigma_{aa} - \Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba}}_{\text{reduced covariance}}\big)
$$

## Definition
$$
\begin{bmatrix} a \\ b \end{bmatrix} \sim \mathcal{N}\!\left(\begin{bmatrix} \mu_a \\ \mu_b \end{bmatrix}, \begin{bmatrix} \Sigma_{aa} & \Sigma_{ab} \\ \Sigma_{ba} & \Sigma_{bb} \end{bmatrix}\right)
\;\Longrightarrow\;
a \mid b \sim \mathcal{N}\big(\mu_{a\mid b},\, \Sigma_{a\mid b}\big),
$$
$$
\mu_{a\mid b} = \mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(b - \mu_b), \qquad
\Sigma_{a\mid b} = \Sigma_{aa} - \Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba}.
$$

## Intuition
Observing part of a jointly Gaussian vector moves the mean of the rest along the regression line and shrinks its covariance by the part the observation explains. The result is again Gaussian, and how much the uncertainty shrinks does not depend on the value observed, only on the fact that it was observed.

## Key results
- $\Sigma_{a\mid b}$ is the Schur complement of $\Sigma_{bb}$ and is independent of the observed $b$, so posterior uncertainty can be computed before any data arrive.
- **Linear-Gaussian measurement form.** With prior $x \sim \mathcal{N}(\mu, P)$ and $y = Cx + v$, $v \sim \mathcal{N}(0, R)$ independent of $x$: $\Sigma_{xy} = PC^\top$, $\Sigma_{yy} = CPC^\top + R$, hence
$$
x \mid y \sim \mathcal{N}\big(\mu + K(y - C\mu),\ (I - KC)P\big), \qquad K = PC^\top (CPC^\top + R)^{-1}.
$$
- **Precision form.** With $\Lambda = \Sigma^{-1}$, $\Sigma_{a\mid b} = \Lambda_{aa}^{-1}$ and $\mu_{a\mid b} = \mu_a - \Lambda_{aa}^{-1}\Lambda_{ab}(b - \mu_b)$. Conditioning is easy in precision form; marginalising is easy in covariance form.

## Connections
- This is [[bayes-rule]] in closed form: a Gaussian prior with a linear-Gaussian likelihood is conjugate.
- The measurement form above is exactly the update step of the [[kalman-filter]]; data-independence of $\Sigma_{a\mid b}$ is why the Kalman covariance recursion can run offline.
- The [[gaussian-process]] posterior is this formula with $a = f(x_*)$ and $b = y$.
- $\Sigma_{ab}\Sigma_{bb}^{-1}$ is the population regression coefficient of $a$ on $b$ ([[linear-regression]]): the conditional mean is the best linear predictor.

## Open questions
