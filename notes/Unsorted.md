
## Linear classification (BCI)
4 types of distributions: circular/same, Gaussian/same, Gaussian/different, non-Gaussian. Only /same handled here

Classification function $f(x)=w^Tx+b$ **(EXPLORE: This is also a feedforward layer - activation. Can such layers be reframed into lin trans too?**, decision boundary $H = ax+b \rightarrow w \perp H$, $dist(\vec{0}, H) = \frac{-b}{||w||}$
Classifier $\begin{cases} \text{the one} & f(x) > 0 \\ \text{the other} & f(x) < 0 \end{cases}$
$dist(x, H) = \frac{f(x)}{||w||}$ (further = generally more confident of classification)
Maybe useful for later to tie stuff together: linear classification is a form of projection onto a lower dimension (similar to PCA, eigen, etc)

$m_k$ mean of class $C_k$ 
$|C_k| = N_k$
Covariance matrix of class $C_k = s_k = \frac{\sum_{n \in C_k} (x_n-m_k)(x_n-m_k)^T}{N_k-1}$

Total within-class covariance matrix: $S_W = \frac{1}{2}(s_1 + s_2)$ for balanced classes, otherwise $S_W = \frac{\sum N_k s_k}{N}$
Between-class covariance matrix: $S_B = (m_2-m_1)(m_2-m_1)^T$
**What do these mean intuitively?**

### Fisher criterion (finding $w$ and $b$)
$$J(w)=\frac{(m_2-m_1)^2}{s_1^2+s_2^2} \text{ (projected space)} = \frac{w^Ts_Bw}{w^Ts_Ww} \text{ (original space)}$$
For best projection, maximize distance, minimize within-class variance: $argmax_w \text{ } J(w)$
To argmax, differentiate by $w$, assume Linear Discriminant Analysis, solve for $\frac{dJ(w)}{dw}=0$ and $\frac{dJ(w)}{db}=0$, $w = S_W^{-1}(m_2-m_1)$, $b = - \frac{w^T(m_1+m_2)}{2}$

**TODO: Ordinary Least Squares, gradient of J**

## KBAI
![[Pasted image 20260909162953.png]]
Flow networks (week 2, slides 72-84), to maximize flow: Ford-Fulkerson method (find edge with min unused capacity (bottleneck), try to draw line from sink s to source t (augmenting path, how is unspecified), add the delta capacity to the bottleneck edge, add -delta capacity to the other edges in the line but with reverse direction (residual edges)), max-flow min-cut theorem proves it.