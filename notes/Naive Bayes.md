$$P(class|feature) = \frac{P(feature|class)P(class)}{P(feature)}$$

It's naive because it assumes all features are mutually independent, so calculation on multiple features is simply:
$$P(class, features) = P(class) \prod P(feature_i|class)$$
$$P(class | features) \propto \overbrace{P(class)}^\text{class prior} \cdot \prod \overbrace{P(feature_i|class)^{feature_i}}^\text{likelyhood of class | feature}$$
