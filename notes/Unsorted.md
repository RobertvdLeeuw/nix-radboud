
## LDA (BCI)
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

### Fisher criterion (finding $w$ and $b$)
$$J(w)=\frac{(m_2-m_1)^2}{s_1^2+s_2^2} \text{ (projected space)} = \frac{w^Ts_Bw}{w^Ts_Ww} \text{ (original space)}$$
For best projection, maximize distance, minimize within-class variance: $argmax_w \text{ } J(w)$
To argmax, differentiate by $w$, assume Linear Discriminant Analysis, solve for $\frac{dJ(w)}{dw}=0$ and $\frac{dJ(w)}{db}=0$, $w = S_W^{-1}(m_2-m_1)$, $b = - \frac{w^T(m_1+m_2)}{2}$


## KBAI
![[Pasted image 20260909162953.png]]
Flow networks (week 2, slides 72-84), to maximize flow: Ford-Fulkerson method (find edge with min unused capacity (bottleneck), try to draw line from sink s to source t (augmenting path, how is unspecified), add the delta capacity to the bottleneck edge, add -delta capacity to the other edges in the line but with reverse direction (residual edges)), max-flow min-cut theorem proves it.


## Logistic regression (FDTM)
$$\text{Sigmoid: } g(x) = \frac{1}{1+e^{-x}}, \space h(x) =g(w^Tx) = \frac{1}{1+e^{-w^Tx+b}}, \space g'(x) = g(z)(1-g(z))$$

![[Pasted image 20260914153622.png|696]]

$$ p(y=1|x, w) = h_w(x) \land p(y=0|x, w) = 1- h_w(x) \rightarrow \text{Hypothesis function: } p(y|x, w) = h_w(x)^y (1-h_w(x))^{1-y}$$
$$\text{Likelyhood of best weights: }\mathcal{L}(w) = p(\vec{y}|X, w) = \prod h_w(x^{(i)})^{y^{(i)}} (1-h_w(x^{(i)}))^{1-y^{(i)}}$$
$$\text{Max log likelyhood: log of } \prod \text{is hard, and } a > b \rightarrow log(a) > log(b) \text{, so }log(\mathcal{L}(w)) = l(w) = \sum y^{(i)} log(h(x^{(i)}))+(1-y^{(i)}) log(1-h(x^{(i)})), \space \frac{\partial l(w)}{\partial w_i} = \sum y^{(i)}-h(x^{(i)})x_j^{(i)}$$

## Random Variables (PT)
$$\text{Random variable } X: S \rightarrow \mathbb{R} \text{, with outcome space S, or with outcome space } \ohm \text{ and outcomes } \omega:X(\omega) \in \mathbb{R}$$
$$Range(X) = R_X = \text{set of possible values for }X, Range(T)=R_T=\{t \in \mathbb{R} | t \ge 0\} = \text{lifetime }T$$
## Gradient Descent:
$$\text{For min/max of function } f(x):  f'(x) = 0  \rightarrow \begin{cases} \text{min} & f''(x) > 0 \\ \text{max} & f''(x) < 0 \\ \text{inconclusive} & f''(x) = 0 \end{cases}$$
$$\text{For multiple dimensions} f(\vec{x}): \nabla f(\vec{x}) = 0  \rightarrow \begin{cases} \text{min} & \nabla^2 f(\vec{x}) > 0 \\ \text{max} & \nabla^2 f(\vec{x}) < 0 \\ \text{saddle} & \nabla^2 f(\vec{x}) = 0 \end{cases}$$$$\text{If only 2D, a simpler way is using } det(\nabla^2 f(\vec{x})) = D = f_{xx}f_{yy}-(f_{xy})^2 
\rightarrow \begin{cases} 
\text{local min} & D > 0 \space \land f_{xx} > 0 \\
\text{local max} & D > 0 \space \land f_{xx} < 0 \\
\text{saddle} & D < 0 \\
\text{inconclusive} & D = 0 \\
\end{cases}$$

## ICA (BCI)
$$x(t) = As(t) \text{ , where } A \in \mathbb{R}^{D \times D} \rightarrow s(t) = Wx(t) \text{ where } W \in \mathbb{R}^{N \times N}$$
$$\hat{s}_i=(w^{(i)})^T X \text{ (optimizing a single filter/col of W for a single source)}$$
Initialize $w$, loop until convergence: GD step towards $\hat{s}$ kurtosis maximizing or minimizing direction
Unlabeled data, independent components (maximize independence - minimized covariance?
	Kurtosis hard to compute, so substitute with other measures of non-Gaussiansuch as negentropy (maximize), mutual information (minimize), likelyhood (maximize), etc 
Unmix mixed signals

ICA is underdetermined: can't determine variances, signs, or order of indipendent components
Noisy data -> multiple component breakdowns: match components, pool data, test unmixing matrix on other data
More sources than sensors: reduce with PCA, less sources than sensors: avoid arbitrary splits by (adding artifact signals?)














Assumptions: linear mixing of signals, at least n-1 non-Gaussian sources, sources statistically independent at time t

CLT states that mixing non-Gaussian stuff makes it more Gaussian -> unmixing makes less Gaussian -> unmix using least Gaussian components
	Gaussian distribution have excess kurtosis of 0 (Pearson kurtosis of -3)
	Solving ICA -> maximize excess kurtosis -> 