Bagging (reduces variance) - bootstrap aggregating

Bootstrap sample = sample data with replacement

Random forest
- Make bootstrapped dataset
- Make decision tree with random combination of features
	- No max tree depth
- Train on bootstrapped data
- Repeat n times
- Prediction: majority vote by all trees
	- Test error on data not in bootstrapped: Out of bag samples
	- For each sample, find trees where sample not in bag, then predict and majority vote using those trees


Boosting (reduces bias)
	Combine weak learners (classifier with slight correlation) together into a strong learner


$$\text{SSE: } L(h(x), y) = \frac{1}{n} \sum_i^n (h(x_i) - y_i)^2$$

Adaboost (adaptive boosting) UPDATE THESE
- Assign weight to all samples (usually starts as $\frac{1}{N}$)
- Fit a stump (tree with singular decision) wrt the weights
- Assess stump score, assign importance rate $\alpha = \frac{1}{2}ln(\frac{1-e_t}{e_t})$
- Increase weights of high error samples depending on $\alpha$
- Decrease weights of low error samples depending on $\alpha$
- Repeat n times


Gradient boosting (fits trees on pseudo-residuals)
$$F_t(x) = (\sum_{i=2}^{t} \alpha h_i(x)) + C$$
- Start with easy initial prediction (for instance, mean of data)
- Compute pseudo-residuals of all samples $-\frac{\partial}{\partial F(x_i)} L(y_i, F(x_i))$ or $y_1 - F(x_1)$
- Fit tree to predict these p-r's, add to ensemble
- Re-predict samples using ensemble, update p-r's
- Repeat n times
