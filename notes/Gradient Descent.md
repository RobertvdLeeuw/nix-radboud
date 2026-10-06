$$\text{For min/max of function } f(x):  f'(x) = 0  \rightarrow \begin{cases} \text{min} & f''(x) > 0 \\ \text{max} & f''(x) < 0 \\ \text{inconclusive} & f''(x) = 0 \end{cases}$$
$$\text{For multiple dimensions} f(\vec{x}): \nabla f(\vec{x}) = 0  \rightarrow \begin{cases} \text{min} & \nabla^2 f(\vec{x}) > 0 \\ \text{max} & \nabla^2 f(\vec{x}) < 0 \\ \text{saddle} & \nabla^2 f(\vec{x}) = 0 \end{cases}$$$$\text{If only 2D, a simpler way is using } det(\nabla^2 f(\vec{x})) = D = f_{xx}f_{yy}-(f_{xy})^2 
\rightarrow \begin{cases} 
\text{local min} & D > 0 \space \land f_{xx} > 0 \\
\text{local max} & D > 0 \space \land f_{xx} < 0 \\
\text{saddle} & D < 0 \\
\text{inconclusive} & D = 0 \\
\end{cases}$$
