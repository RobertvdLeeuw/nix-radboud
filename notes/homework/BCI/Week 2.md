2a $S \in \mathbb{R}^{D \times D}$

2b $\overline{x}^{(0)} = \frac{1+3+5}{3} = 3$
$\overline{x}^{(1)} = \frac{2+4+6}{3} = 4$

$$(\overline{X}-X)=
\begin{bmatrix}
3-1 & 4-2 \\
3-3 & 4-4 \\
3-5 & 4-6 \\
\end{bmatrix} 
=
\begin{bmatrix}
2 & 2 \\
0 & 0 \\
-2 & -2 \\
\end{bmatrix}
$$
$$(\overline{X}-X)^T(\overline{X}-X)
=
\begin{bmatrix}
2 & 0 & -2 \\
2 & 0 & -2 \\
\end{bmatrix}
\begin{bmatrix}
2 & 2 \\
0 & 0 \\
-2 & -2 \\
\end{bmatrix}
=
\begin{bmatrix}
2(2)+0(0)-2(-2) & 2(2)+0(0)-2(-2) \\
2(2)+0(0)-2(-2) & 2(2)+0(0)-2(-2) \\ 
\end{bmatrix}
=
\begin{bmatrix}
8 & 8 \\
8 & 8 \\ 
\end{bmatrix}
$$
$$Cov(X) = \frac{(\overline{X}-X)^T(\overline{X}-X)}{n-1} = \begin{bmatrix} 4 & 4 \\ 4 & 4 \end{bmatrix}$$
3:
A: S5, B: S2, C: S1, D: S3, E: S4
