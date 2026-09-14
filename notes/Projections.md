## PCA
PCA determines a linear subspace (1 move mean of data to zero point, 2 rotate such that eigenvectors form new axes, 3 optionally scale data)
Assumption: relevance is expressed by variance (which also includes noise/outliers/scaling/etc)
	Dimensional reduction with PCA assumes only directions with high variance are important (eigenvectors with highest eigenvalues)

Objective: preserve maximal variance

### Unit vector u (magnitude of 1, only direction)
$$u^Tu=1 \text{ constrained to maximizing variance doesn't grow to infinity}$$
$$\text{Mean of projected data } = u^T \overline{x}, \space \overline{x} = \frac{\sum_n^{N}x_n}{N}$$
$$\text{To max variance: } argmax_u \sum_n^N (u^Tx_n - u^Y \overline{x}) = argmax_u u^T S u \text{ (where S is cov matrix)}$$
$$\text{Same thing but constrained: } argmax_{u, \lambda} \space u^T S u + \lambda (1 - u^Tu)$$
$$\frac{\partial f}{\partial\lambda} = 0 \rightarrow 1 = u^T u, \space \frac{\partial f}{\partial u} = 0 \rightarrow 0 = Su - \lambda u$$$$\text{Fumble that about and you get }Su=\lambda u \text{ where S is cov mat, u is (L2 normalized) eigenvector,} \lambda = \text{eigenvalue}$$
For multiple eigenvectors, they should be orthogonal
### Open Questions
- Orthogonal ($u^T X u$) vs oblique projection ($u^{-1}Xu$)
-