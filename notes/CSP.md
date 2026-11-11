Supervised feature extraction (binary labels)
Extracts oscillatory features from multi-channel recording

Does linear decomp into subspace components, represented by spatial filters
	A spacial filter $w^TX$ enhances or suppresses contribution from certain channels
	
Goal of CSP is to find 2 spacial unmixing filters for contrast enhancement between conditions, where:
- Each filter delivers one virtual (CSP) channel
- Each filter maximizes bandpower (approx. narrowband variance) for one class, but minimizes for the other

CSP requires 2 filtering operations: frequency (bandpass to alpha) and spatial with CSP filters

Analytical solution:
$$W: \text{ each column = spatial filter, }D: \text{ diagonal matrix where diagonal is eigvals in } W, \Sigma_i = \text{ Cov mat of class i}$$
$$W^T \Sigma_1W=D $$
$$W^T(\Sigma_1 + \Sigma_2)W = I$$
$$\Sigma_1 w_j = \lambda_j \Sigma_2 w_j$$
Applying one spatial filter $W_j$ to X results in a single, spatially filtered time series signal (CSP channel)

Simple selection metrics: component with most extreme eigvals, or most discriminative components like r^2 or AUC

ERD/ERS curve represents change in signals envelope power over time, relative to pre-event baseline period

CSP is sensitive to outliers (due to being based on variance)

Optimization formulation (Rayleigh quotient):
$$argmax_W \frac{W^T (\Sigma_1 - \Sigma_2) W}{W^T (\Sigma_1 + \Sigma_2) W} \text{ or } argmax_W \frac{W^T \Sigma_1 W}{W^T \Sigma_2 W}$$

Find spatial intuitions for this
- Whiten wrt $\Sigma_1 + \Sigma_2$ 
- rotation of eigvecs from new CSP axes
![[Pasted image 20261110203649.png]]
