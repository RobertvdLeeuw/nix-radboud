$$x(t) = As(t) \text{ , where } A \in \mathbb{R}^{D \times D} \rightarrow s(t) = Wx(t) \text{ where } W \in \mathbb{R}^{N \times N}$$
$$\hat{s}_i=(w^{(i)})^T X \text{ (optimizing a single filter/col of W for a single source)}$$
Initialize $w$, loop until convergence: GD step towards $\hat{s}$ kurtosis maximizing or minimizing direction
Unlabeled data, independent components (maximize independence - minimized covariance?
	Kurtosis hard to compute, so substitute with other measures of non-Gaussiansuch as negentropy (maximize), mutual information (minimize), likelyhood (maximize), etc 
Unmix mixed signals

ICA is underdetermined: can't determine variances, signs, or order of independent components
Noisy data -> multiple component breakdowns: match components, pool data, test unmixing matrix on other data
More sources than sensors: reduce with PCA, less sources than sensors: avoid arbitrary splits by (adding artifact signals?)
Assumptions: linear mixing of signals, at least n-1 non-Gaussian sources, sources statistically independent at time t, n sources <-> n sensors

CLT states that mixing non-Gaussian stuff makes it more Gaussian -> unmixing makes less Gaussian -> unmix using least Gaussian components
	Gaussian distribution have excess kurtosis of 0 (Pearson kurtosis of -3)
	Solving ICA -> maximize excess kurtosis -> 
