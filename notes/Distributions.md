
## Bernioulli: $X \sim Bern(p)$
Flip a coin
$\mathcal{S} = \{0, 1\}$

## Binomial: $X \sim Binomial(N, p)$
N independent Bernoulli trials
$\mathcal{S} = \{0,1,\dots, N\}$
$P_X(k) = {N \choose k} p^k (1-p)^{N-k}$

## Geometric: $X \sim Geometric(p)$
Consider a coin with $P (H) = p$. Toss the coin $k$ times until first Heads. How many tosses?
$P_X(k) = p(1-p)^{k-1}$

## Hypergeometric: $X \sim HypGeom(n, s, m), \space m \le n, \space s \le n$
$n$ total items of which $s$ blue. Pick $m$ items at random, get $X$ blue
$P_X(k) = \frac{{s \choose k}{n-s \choose m-k}}{n \choose m}$
$S_X = \{k \in N \space | \space max(0, m + s − n) \le k \le min(s, m)\}$

## Poisson: $X \sim Poisson(\lambda), \space \lambda > 0$
probability of a given number of events occurring in a fixed interval of time if these events occur with a known constant mean rate and independently of the time since the last event
$P_X(k) = \frac{\lambda^k}{k!}e^{- \lambda} \text{ where } \lambda = \text{ expected n events in interval, } k = \text{ actual n events accured in same interval}$

