## Random Variables
$$\text{Random variable } X: S \rightarrow \mathbb{R} \text{, with outcome space S, or with outcome space } \ohm \text{ and outcomes } \omega:X(\omega) \in \mathbb{R}$$
$$Range(X) = R_X = \text{set of possible values for }X, Range(T)=R_T=\{t \in \mathbb{R} | t \ge 0\} = \text{lifetime }T$$
## Expectation
$\mathbb{E}[X] = \sum_{s \in S} X(s)P(s) = \sum_{x \in R_x} xP_X(x)$
Constants: $c \in \mathbb{R} \Rightarrow \mathbb{E}[\text{c}] = \text{c}$
Linear adding: $\mathbb{E} [aX + bY] = a\mathbb{E}[X] + b\mathbb{E}[Y] \text{, regardless of whether X and Y are independent}$
$\mathbb{E}[\mathbb{E}[X]] = \mathbb{E}[X], \space \mathbb{E}[X] \cdot \mathbb{E}[X] = (\mathbb{E}[X])^2, \space \mathbb{E}[\mathbb{E}[X]^2] = \mathbb{E}[X]^2, \space \mathbb{E}[X \cdot \mathbb{E}[X]] = \mathbb{E}[X] \cdot \mathbb{E}[X]$

### Variance:
$Var[X] = \mathbb{E}[(X - \mu_X)^2]$
$Var[X] \ge 0, \space \text{X is constant (takes 1 value)} \Rightarrow Var[X] = 0, \space Var[X+c] = Var[X]$
$Var[\alpha X] = \alpha^2 Var[X], \space Std[ \alpha X] = |\alpha| Std[X]$
$Var[X] = \mathbb{E}[X^2] - \mathbb{E}[X]^2$
If X and Y independent: $Var[X+Y] = Var[X] + Var[Y]$
$Var[X+Y] = Var[X] + Var[Y] + 2Cov[X, Y]$

### Covariance
$Cov[X, Y] = \mathbb{E}[XY]-\mathbb{E}[X]\mathbb{E}[Y] = \mathbb{E}[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])]$
$Cov[X, c] = 0$
$Cov[\alpha X, Y] = \alpha Cov[X, Y]$
$Cov[X+Y, Z] = Cov[X, Z]+Cov[Y, Z]$

Pearson correlation: $\frac{Cov[X, Y]}{\sqrt{Var[X]Var[Y]}}$
## Bernioulli: $X \sim Bern(p)$
Flip a coin
$\mathcal{S} = \{0, 1\}$
$\mathbb{E}[X] = p$
$Var[X] = p-p^2 = p(p-1)$

## Binomial: $X \sim Binomial(N, p)$
N independent Bernoulli trials
$\mathcal{S} = \{0,1,\dots, N\}$
$P_X(k) = {N \choose k} p^k (1-p)^{N-k}$
$\mathbb{E}[X] = \mathbb{E}[X_1] + \mathbb{E}[X_2]+ \dots = \overbrace{p \cdot p \cdot \dots}^{n \text{ times}} = n \cdot p$
$Var[X] = np(p-1)$

## Geometric: $X \sim Geometric(p)$
Probability of $k$ Bernoulli trials resulting in only last trial succeeding, ie. $P(\text{Binomial}(k-1) = 0) * p$

$P_X(k) = p(1-p)^{k-1}$

## Uniform: $X \sim Unif(a, b)$
$\mathbb{E}[X] = \frac{1}{b-a} \int_a^b u du = \frac{1}{2}(a+b)$
$Var[X] = \frac{(b-a)^2}{12}$

## Hypergeometric: $X \sim HypGeom(n, s, m), \space m \le n, \space s \le n$
$n$ total items of which $s$ blue. Pick $m$ items at random, get $X$ blue
$P_X(k) = \frac{{s \choose k}{n-s \choose m-k}}{n \choose m}$
$S_X = \{k \in N \space | \space max(0, m + s − n) \le k \le min(s, m)\}$

## Poisson: $X \sim Poisson(\lambda), \space \lambda > 0$
Probability of a given number of events occurring in a fixed interval of time if these events occur with a known constant mean rate and independently of the time since the last event
$P_X(k) = \frac{\lambda^k}{k!}e^{- \lambda} \text{ where } \lambda = \text{ expected n events in interval, } k = \text{ actual n events accured in same interval}$

Can be approximated with Binomial: stack short intervals as Bernoulli's. Same vice versa: $\lambda = np$
$\mathbb{E}[X] = np = n \frac{\lambda}{n} = \lambda$
$Var[X] = np(p-1) = n \frac{\lambda}{n}(1-\frac{\lambda}{n}) = \lambda(1-\frac{\lambda}{n})$

## Exponential: $X \sim Exponential(\lambda)$
$f_X(x)=\begin{cases} \lambda e ^{-\lambda x} & x>0 \\ 0 & x \le 0 \end{cases} \space , \space F_X(x)=\begin{cases} 1 - e ^{-\lambda x} & x>0 \\ 0 & x \le 0 \end{cases}$
$\mathbb{E}[X]=\frac{1}{\lambda}$
$Var[X]=\frac{1}{\lambda^2}$

## Gaussian: $X \sim \mathcal{N}(\mu, \sigma^2)$
$$f_X(x)=\frac{1}{\sigma \sqrt{2 \pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}} \space , \space F_X(X \le x) = \phi(\frac{x-\mu}{\sigma}) \space , \space \phi(x)=P(X \le x) = \frac{1}{\sqrt{2 \pi}} \int_{-\infty}^x e^{-\frac{u^2}{2}}du$$
$\mathbb{E}[X]=\mu$
$Var[X]=\sigma^2$
CLT states that $\frac{X-\mu}{\sigma} \approx$ normally distributed

## Transformations (monotonic: $y = g(x)$)
$$\text{CDF: } F_Y(y) = F_x(g^{-1}(y))\text{ if g > 0 else } 1 - F_x(g^{-1}(y))$$
$$\text{PDF: } f_y(y) = f_x(g^{-1}(y)) | \frac{d}{dy}g^{-1}(y) |$$
