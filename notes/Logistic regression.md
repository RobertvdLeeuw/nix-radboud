$$\text{Sigmoid: } g(x) = \frac{1}{1+e^{-x}}, \space h(x) =g(w^Tx) = \frac{1}{1+e^{-w^Tx+b}}, \space g'(x) = g(z)(1-g(z))$$
$$J(w) = ||H_w(x), y||^2 \text{ but quadratic, so easier to use: } J(w) = y \cdot \overbrace{-ln(H_w(x))}^{\text{cost if }y=1} - ((1-y)\overbrace{ln(1-H_w(x))}^{\text{cost if }y=0})$$
![[Pasted image 20260914153622.png|696]]

$$ p(y=1|x, w) = h_w(x) \land p(y=0|x, w) = 1- h_w(x) \rightarrow \text{Hypothesis function: } p(y|x, w) = h_w(x)^y (1-h_w(x))^{1-y}$$
$$\text{Likelyhood of best weights: }\mathcal{L}(w) = p(\vec{y}|X, w) = \prod h_w(x^{(i)})^{y^{(i)}} (1-h_w(x^{(i)}))^{1-y^{(i)}}$$
$$\text{Max log likelyhood: log of } \prod \text{is hard, and } a > b \rightarrow log(a) > log(b) \text{, so }log(\mathcal{L}(w)) = l(w) = \sum y^{(i)} log(h(x^{(i)}))+(1-y^{(i)}) log(1-h(x^{(i)}))$$
$$\frac{\partial l(w)}{\partial w_i} = \sum y^{(i)}-h(x^{(i)})x_i^{(i)}$$
