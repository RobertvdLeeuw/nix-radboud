2a $S \in \mathbb{R}^{D \times D}$
2b $\overline{x}^{(0)} = \frac{1+3+5}{3} = 2 \frac{2}{3}$
$Var(X^{(0)}) = \frac{\sum (x_i - \overline{x}^{(0)})^2}{n-1} = \frac{(2\frac{2}{3}-1)^2+(-\frac{1}{3}-3)^2+(2\frac{2}{3}-5)^2}{2} = \frac{(1\frac{2}{3})^2+(-\frac{1}{3})^2+(-2\frac{1}{3})^2}{2} = \frac{\frac{25}{9}+\frac{1}{9}+\frac{49}{9}}{2} = \frac{75}{18} = 4 \frac{3}{18} = 4 \frac{1}{6}$

$\overline{x}^{(1)} = \frac{2+4+6}{3} = 4$
$Var(X^{(1)}) = \frac{\sum (x_i - \overline{x})^2}{n-1} = \frac{(2 - 4)^2+(4 - 4)^2+(6 - 4)^2)}{2} = \frac{4+0+4}{2} = \frac{8}{2} = 4$

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
