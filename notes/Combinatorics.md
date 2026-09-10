Hell comes from different selections on different pools, with some part ordered and some unordered. Break down stuff into independent, atomic stages/pools until the base cases below are reached. From there, reconstruct.

| Single pool, single selection | Ordered                               | Unordered                                   |
| ----------------------------- | ------------------------------------- | ------------------------------------------- |
| **w/ replacement**            | $n^k$                                 | ${{n+k-1} \choose n}$ ($n$ stars, $k$ bars) |
| **w/o replacement**           | $\frac{n!}{(n-k)!} = {n \choose k}k!$ | ${n \choose k} = \frac{n!}{k!(n-k)!}$       |
## Decomposition rules
- **Different pools, item(s) from each, order among pools doesn't matter:** $m$ red marbles, $m'$ picked, $m$ blue marbles, $m'$ picked $\rightarrow {m \choose m'}  \times {n \choose n'}$ 
- **Constraint is 'at least/at most/none' about 1 pool:** complement
- **1 pool, ordered selection with duplicates in pool:** $n$ objects with $n_1$ identical, $n_2$ identical, ... $\rightarrow \frac{n!}{n_1!n_2! \dots}$ permutations (unique jugglings of the letters in STATISTICS - S thrice, T thrice, I twice, rest once $\rightarrow \times 1! =  \times 1 \rightarrow$ ignored) 
- **Lower bound per bin, unordered:** Stars-bars with minimum in certain bins $\rightarrow n' = n - n_\text{reserved}, {{n'+k-1} \choose {n'}}$ combinations
- **FLESH OUT FURTHER (WORK IN: THOSE BASE CASES ARE THEMSELVES ALSO DECOMP RULES!!)**
 

## Other, Unsorted PT Stuff
$U$ = outcome set $S$, events $E \subset S$ (or $E \subseteq S$?)
Assumptions: $S$ is finite ($|S| = n$), all outcomes equiprobable




