## TODO
- DDOF
- Figure out how median relates to var-skew
- Taylor series connection
- Coskew and cokurt

## First Order: Mean
$$\mu= \frac{\sum_x^X x}{n}$$
But this can't distinguish between spread: (1, 2, 3, 4, 5) vs (3, 3, 3, 3, 3)
### Why no comean?
Same reason there's no first order equivalent to $\frac{\partial^2 f}{\partial x \partial y}$ (Taylor Series stuff connects this further)
## Second Order: Variance 
$$\text{Crude: } \frac{\sum_x^X x^2}{n} \text{ , Centered: } \sigma^2 = \frac{\sum_x^X (x-\mu)^2}{n}$$
But this can't distinguish between direction of spread (squaring cancels sign): (1, 1, 1, 1, 6) and (-1, 1, 2, 3, 5)
### Covariance
This is actually the general case.
$$Cov(X, Y) = \frac{\sum_x^X \sum_y^Y (x-\overline{x})(y-\overline{y})}{n}$$

Because we no longer square, we preserve the sign again.
Positive means positive correlation, negative means negative correlation. Cannot distuingish between correlation strength and feature scaling.

Covariance Matrix: $\begin{bmatrix} Var(x) & Cov(x, y) \\ Cov(y, x) & Var(y) \end{bmatrix} = \frac{(X - \overline{X})^T(X - \overline{X})}{n-1}$
### Correlation
$Corr(x, y) = \frac{Cov(x, y)}{\sqrt{Var(x)}\sqrt{Var(y)}}$
Normalized $[-1, 1]$ values which signal correlation strength as well.

## Third Order: Skewness
With an odd power, we got sign back.
$$\text{Crude: } \frac{\sum_x^X x^3}{n} \text{ , Centered: } \sigma^2 = \frac{\sum_x^X (x-\mu)^3}{n} \text{ , Standardized: } \frac{\sum_x^X (x-\mu)^3}{n\sigma^3} $$
But this can't distinguish between (???) and (???)
## Fourth Order: Kurtosis
Symmetric again, but fourth power makes tails (extreme deviations) weight far more heavily
$$\text{Crude: } \frac{\sum_x^X x^4}{n} \text{ , Centered: } \sigma^2 = \frac{\sum_x^X (x-\mu)^4}{n} \text{ , Standardized: } \frac{\sum_x^X (x-\mu)^4}{n\sigma^4} $$
But this can't distinguish between (???) and (???)


