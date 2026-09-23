
$$\frac{df(x)}{dx} = f'(x) = \lim_{\Delta x \rightarrow 0} \frac{f(x + \Delta x) - f(x)}{\Delta x}$$
$$\frac{\partial f(x_0, x_1)}{\partial x_0} =  \lim_{\Delta x_0 \rightarrow 0} \frac{f(x_0 + \Delta x_0, x_1) - f(x_0, x_1)}{\Delta x_0} \text{ (treat other inputs/dims like constants)}$$
$$\frac{\partial^2f}{\partial x \partial y} = \frac{\partial^2f}{\partial y \partial x}$$

Inference

| Product  | $[uv]' = u'v+uv'$                      | $\frac{d}{dx}uv = \frac{du}{dx}v+u\frac{dv}{dx}$            |
| -------- | -------------------------------------- | ----------------------------------------------------------- |
| Quotient | $[\frac{u}{v}]' = \frac{u'v-uv'}{v^2}$ | $\frac{du}{dx} = \frac{\frac{du}{dx}v-u\frac{dv}{dx}}{v^2}$ |
| Chain    | $[u(v)]' = u'(v)v'$                    | $\frac{du}{dx} = \frac{du(v)}{dv} \cdot \frac{dv}{dx}$      |

Common derivatives

| $u^n$      | $nu^{n-1}u'$           |
| ---------- | ---------------------- |
| $e^{u}$    | $u'e^{u}$              |
| $ln(u)$    | $\frac{u'}{u}$         |
| $a^u$      | $a^ul n(u) u'$         |
| $\sqrt{u}$ | $\frac{u'}{2\sqrt{u}}$ |
| $sin(u)$   | $cos(u)u'$             |
| $cos(u)$   | $-sin(u)u'$            |
| $tan(u)$   | $sec^2(u)u'$           |
| $sec(u)$   | $sec(u)tan(u)u'$       |
| $cot(u)$   | $-csc^2(u)u'$          |
| $csc(u)$   | $-csc(u)cot(u)u'$      |

## Function Approximation
$$\text{Maclauren series: } f(x) @ 0 \approx f(0) + \frac{f'(0)}{1!}x + \frac{f''(0)}{2!}x^2 + ... = \sum_i^n \frac{\frac{d^1}{dx^i}f(0)x^i}{i!}$$
$$\text{Taylor series: } f(x) @ a \approx f(a) + \frac{f'(a)}{1!}(x-a) + \frac{f''(a)}{2!}(x-a)^2 + ... = \sum_i^\infty \frac{\frac{d^1}{dx^i}f(a)(x-a)^i}{i!}$$


## Multivariable
Multivariable f(...) = >1 input, 1 output, multivariate $\vec{g}(\dots)$ = >1 input, >1 output 

$$\text{Gradient of } J = \nabla J = \text{ vector of all first-order partial derivatives}$$
$$\text{Hessian of } J = \nabla^2 J = \text{ matrix of all second-order partial derivatives}$$$$\text{Taylor Series: } f(\vec{x}) \approx P(\vec{x}) = f(\vec{a}) + \nabla f(\vec{a})^T(\vec{x} - \vec{a}) + \frac{(\vec{x} - \vec{a})^T \nabla^2 f(\vec{a})(\vec{x} - \vec{a})}{2!}+ \dots = \sum_i^\infty \frac{\nabla^i f(\vec{a})(\vec{x}-\vec{a})^i}{i!}$$
## Multivariate/vector
$$\frac{df}{dt} = \frac{\partial f}{\partial x} \frac{dx}{dt} + \frac{\partial f}{\partial y} \frac{dy}{dt}$$
$$\text{Jacobian matrix: } J_f \in R^{m \times n}, \space [J_f]_{ij} = \frac{\partial f_i}{\partial x_j}, \space [J_f]_{i} = (\nabla f_i)^T$$
$$h(\vec{x}) = f(g(\vec{x})) \Rightarrow J_h(\vec{x}) = J_f(g(\vec{x})) \cdot J_g(\vec{x})$$
$$\text{Newton's Method: } \vec{x}_{k+1} = \vec{x}_k + \nabla^2 f(\vec{x}_k)^{-1} \nabla f(\vec{x}_k)$