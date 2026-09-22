
## Expectation
$\mathbb{E}[X] = \sum_{s \in S} X(s)P(s)$
Constants: $c \in \mathbb{R} \Rightarrow \mathbb{E}[\text{c}] = \text{c}$
Linear adding: $\mathbb{E} [aX + bY] = a\mathbb{E}[X] + b\mathbb{E}[Y] \text{, regardless of whether X and Y are independent}$

### Variance:
$Var[X] = \mathbb{E}[(X - \mu_X)^2]$
$Var[X] \ge 0, \space \text{X is constant (takes 1 value)} \Rightarrow Var[X] = 0, \space Var[X+c] = Var[X]$
$Var[\alpha X] = \alpha^2 Var[X], \space Std[\alpha X] = |alpha| Std[X]$
$Var[X] = \mathbb{E}[X^2] - \mathbb{E}[X]^2$
If X and Y independent: $Var[X+Y] = Var[X] + Var[Y]$

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
Consider a coin with $P (H) = p$. Toss the coin $k$ times until first Heads. How many tosses?
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

Can be approximated with Binomial: stack short intervals as Bernoulli's
$\mathbb{E}[X] = np = n \frac{\lambda}{n} = \lambda$
$Var[X] = np(p-1) = n \frac{\lambda}{n}(1-\frac{\lambda}{n}) = \lambda(1-\frac{\lambda}{n})$
