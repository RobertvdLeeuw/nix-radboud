
| Union           | $A \cup B$ | $A \lor B$       |
| --------------- | ---------- | ---------------- |
| Intersection    | $A \cap B$ | $A \land B$      |
| Difference (as) | $A/B, A-B$ | $A \land \neg B$ |

Disjoint sets (no overlap): $A \cap B = \emptyset$

Power set = set of all subsets (including the original set) = $\mathcal{P}(S)$,  $|\mathcal{P}| = 2^n$
**TODO: Explore link between power set and combinations/permutations ([Powers of 2 in Pascal's Triangle](https://artofproblemsolving.com/videos/counting/chapter12/141))**
## Probability stuff
$$P: \mathcal{P}(S) \to [0, 1]$$
$$P(S) = 1 \text{, } P(\emptyset) = 0$$$$P(A^C) = 1 - P(A)$$
$$A \subseteq B \rightarrow P(A) \le P(B)$$
$$P(A \cup B) = P(A) + P(B) - P(A \cap B) \text{ (fix overcount)}$$
$$P(A | B) = \frac{P(A \cap B)}{P(B)} \text{ (B becomes the new outcome space)} \rightarrow P(B|B) = \frac{P(B)}{P(B)}=1$$
$$P(C|A \cap B) = P(C | A,B) = \frac{P(A \cap B \cap C)}{P(A \cap B)} = \frac{P(A, B, C)}{P(A, B)}$$
$$P(A,B) = P(A|B)P(B) \text{, chain rule: } P(A,B, C) = P(A|B,C)P(B,C) = (A|B,C)P(B|C)P(C)$$
**Chain rule results in permutations, some easier to calc than others; selection matters!**

$$\text{Marginalization: } P(B) = \sum_i^n P(B|A_i) \text{ where A is partition of S (disjoint sets that together form S)}$$
$$\text{Bayes' rule: } P(A|B)=\frac{P(B|A)(P(A))}{P(B)} \text{, } P(A|B)P(B)=P(A, B)=P(B|A)P(A)$$
$$P(A|B)=P(A) \text{ (independent) } \not \leftrightarrow P(A|B,C)=P(A|C)  \text{ (conditionally independent) } $$
**TODO: Maybe pairwise vs mutual independence**
### $|S| \le \aleph_0$ (at most countably infinite, mass)
$$\text{If }(A_1, A_2, ..., A_n) \text{ are disjoint, then } P(A_1 \cup A_2 \cup \dots) = \sum_i^n (P(A_i)) $$
###  $\aleph_0 \le |S| \le \aleph_1$ (uncountable, density) (right math notation?)
If uniform probability, then $P([a, b]) = b - a$ and $P(\{x\}) = 0$ for all x (infinitely slim)


