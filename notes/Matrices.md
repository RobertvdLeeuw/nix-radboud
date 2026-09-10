
TODO: Inner (dot) vs outer vs mat mult vs hamarand vs etc
## Products
Dot/inner: $\vec{u} \cdot \vec{v} = \vec{u}^T \vec{v} = \vec{v} \cdot \vec{u} \in \mathbb{R}$
Outer: $\vec{u} \otimes \vec{v} = \vec{u}\vec{v}^T = (\vec{v^T} \otimes \vec{u^T})^T \in \mathbb{R}^{|u| \times |v|}$

## Linear transformations
$$ \text{1 dim: }
\begin{bmatrix}
x
\end{bmatrix} \rightarrow
\begin{bmatrix}
a \\ b
\end{bmatrix}
\begin{bmatrix}
x
\end{bmatrix} = 
\begin{bmatrix}
ax \\ bx
\end{bmatrix}
$$

$$ \text{2 dim: } 
\begin{bmatrix}
  x \\ y
\end{bmatrix} \rightarrow 

\begin{bmatrix}
a \\ c
\end{bmatrix}
\begin{bmatrix}
x
\end{bmatrix}
+
\begin{bmatrix}
b \\ d
\end{bmatrix}
\begin{bmatrix}
y
\end{bmatrix}
=
\begin{bmatrix}
  a & b \\ c & d
\end{bmatrix} 

\begin{bmatrix}
  x \\ y
\end{bmatrix}
= 
\begin{bmatrix}
  ax + by \\ cx + dy
\end{bmatrix}

\text{  (} \begin{bmatrix} a\\c\end{bmatrix} \text{ and } \begin{bmatrix} b\\d\end{bmatrix} \text{ are basis-vectors)}
$$
$$ \text{n-dim:}
\begin{bmatrix}
f_1 \\ f_2 \\ \vdots \\ f_n
\end{bmatrix} \rightarrow

\begin{bmatrix}
w_{11} & w_{12} & \dots & w_{1n} \\
w_{21} & w_{22} & \dots & w_{2n} \\ 
\vdots & \vdots & \ddots  & \vdots \\
w_{n1} & w_{n2} & \dots & w_{nn}
\end{bmatrix}
\begin{bmatrix}
f_1 \\ f_2 \\ \vdots \\ f_n
\end{bmatrix}
=
\begin{bmatrix}
w_{11}f_1 + w_{12}f_2 + \dots + w_{1n}f_n \\
w_{21}f_1 + w_{22}f_2 + \dots + w_{2n}f_n \\ 
\vdots \\
w_{n1}f_1 + w_{n2}f_2 + \dots + w_{nn}f_n
\end{bmatrix}
$$

## Determinants
$$A = M_{n\times n} \text{ , } |det(A)| = \text{the factor by which a transformation matrix scales any area of the input space}$$
$$det(A) \gt 0 \rightarrow \text{orientation preserved, }det(A) \lt 0 \rightarrow \text{orientation flipped}$$

$$det[a] = a$$
$$det\begin{bmatrix}a & b \\ c & d \end{bmatrix} = ad -bc$$
Laplace expansion for nxn matrix, if that ever comes up

## Basis vectors 
$$
\begin{bmatrix}
a \\ c
\end{bmatrix}
\begin{bmatrix}
x
\end{bmatrix}
+
\begin{bmatrix}
b \\ d
\end{bmatrix}
\begin{bmatrix}
y
\end{bmatrix}
 = 
\vec{a}x + \vec{b}y \text{ , } \vec{a} \text{ and } \vec{b} \text{ are basis vectors}
$$

Add how to translate between basis vectors
## Eigen stuff
$$\vec{v} = \text{eigenvector, } A = M_{n\times n} \rightarrow A\vec{v} = \lambda \vec{v} \text{ where eigenvalue = } \lambda \in \mathbb{R}$$
Eigenvector of a transformation matrix/vector = the vector whose direction is not altered by the transformation, only stretched or squashed. Eigenvalue = the factor by which the transformation stretches the eigenvector. Negative eigenvalue = flipped direction

To solve for eigen vector(s) and value(s):
$$(A-\lambda I) \vec{v} = \vec{0} \text{ where } \vec{v} \neq \vec{0}$$
$$det(A-\lambda I) = \prod (A_{ii} - \lambda) = 0$$
All this is somehow a mapping from whatever coordinate system to a lower dimension, figure out how

$$A\text{ : } 
\begin{cases}
A_{ij}=0 & i \neq j \\
A_{ij} = \lambda_i & i = j
\end{cases} \rightarrow \text{simple scaling transformation, every vector is eigen}
$$
**For later: PCA is just eigenvectors on covariance matrix of data.**
### Eigendecomposition
$$A=DQD^{-1} \text{, where } A = \text{eigenvalues, D = diagonal matrix of A, Q = a matrix where each col is an eigenvector}$$
Changing base vector to eigenvectors means every coordinate will be a diagonal matrix (which is much easier to work with) - called eigenbasis
## M squared, M inv, etc`
