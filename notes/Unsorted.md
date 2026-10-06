## KBAI
![[Pasted image 20260909162953.png]]
Flow networks (week 2, slides 72-84), to maximize flow: Ford-Fulkerson method (find edge with min unused capacity (bottleneck), try to draw line from sink s to source t (augmenting path, how is unspecified), add the delta capacity to the bottleneck edge, add -delta capacity to the other edges in the line but with reverse direction (residual edges)), max-flow min-cut theorem proves it.

$$\text{Simulated annealing: } P(\text{accept}) = e^{\frac{f(x) - f(x')}{T}} , \space T_n =  T_{n-1}\cdot\lambda^t$$


## Metrics:
- **Cohens cappa:** inter annotation agreement
- **Jaccard:** classification metric


![[Pasted image 20260928204809.png]]


$$\text{Laplace smoothing: }\theta_j = \frac{x+\alpha}{N+d\alpha} \text{ , where } x \in \mathbb{R}^D \land N = |x|$$

Decision trees: leaf is pure if contains only 1 class, otherwise impure. P1 and P2 should be different for informative split
$$\text{GINI impurity: } GINI(x_i)=1-P_1(True|x_i)^2-P_2(False|x_i)^2 \text{ , total impurity: } GINI(X) = \prod_x^X \frac{|x|}{|X|} GINI(x)$$
For contuinuous variable, test GINI at every split: (x0+x1)/2
## PT
$$\text{Method of transformations: }f_Y(y) = \begin{cases} \frac{f_X(x)}{|g'(x)|} = f_X(x) \cdot |\frac{dx}{dy}| & g(x) = y \\ 0 & g(x) = y \text{ has no real solution} \end{cases}$$
![[Pasted image 20260929150836.png]]![[Pasted image 20260929150949.png]]

Information transfer rate
![[Pasted image 20261003202936.png]]
![[Pasted image 20261003202949.png]]
$$R^2 = 1- \frac{\sum(y_i-\overline{y})^2}{\sum (y_i-f_i)^2}$$

Entropy is the expected amount of information needed to describe the state of a variable: $Entropy(X) = \sum_x^X -p(x)log(p(x))$
![[Pasted image 20261005171627.png]]
![[Pasted image 20261005171709.png]]![[Pasted image 20261005171813.png]]

Max Likelyhood: $L(\text{params}; x_1 \dots x_n) = P(x_1 \dots x_n | \text{params}) = \prod_i^n P_{X_i} (x_i | \text{params})$
Example with Poisson: $\prod_i^n \frac{\lambda^{x_i}}{x_i!}e^{-\lambda}$

Log stuff:
$log(abc) = log(a)+log(b)+log(c), \space a>0, b>0, c>0$
$log(e^a)=a$
$log(a^b)=b \cdot log(a),\space a>0$
$log(\frac 1 a) = log(a^{-1}) = -log(a), \space a>0$

Max log likelyhood: $\mathcal{L}(\text{params};x_1 \dots x_n) = log(L(\text{params};x_1 \dots x_n)) = log(\prod_i^n P_{X_i} (x_i | \text{params})) = \sum^n log(P_{X_i} (x_i | \text{params}))$
Find $\frac{\partial \mathcal{L}}{\partial \text{params}} = 0$
