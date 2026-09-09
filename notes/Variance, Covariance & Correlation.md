$Var(x) = \sigma^2 = \frac{\sum (x_i - \overline{x})^2}{n-1}$

$Cov(x, y) = \frac{\sum (x_i - \overline{x}) (y_i - \overline{y})}{n-1} \Rightarrow Cov(x, x) = Var(x)$
Positive means positive correlation, negative means negative correlation. Doesn't show strength and is sensitive to scaling.

$Corr(x, y) = \frac{Cov(x, y)}{\sqrt{Var(x)}\sqrt{Var(y)}}$
Normalized $[-1, 1]$ values which signal correlation strength as well.

Covariance Matrix: $\begin{bmatrix} Var(x) & Cov(x, y) \\ Cov(y, x) & Var(y) \end{bmatrix} = (X - \overline{X})^T(X - \overline{X})$

## Open Questions
- When/why n vs n-1?