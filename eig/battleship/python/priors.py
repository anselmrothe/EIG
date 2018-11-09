from ...bayes import Distribution, normalize
from collections import Counter
import numpy as np

class EqualSizesDistribution(Distribution):
    def __init__(self, ship_labels):
        self.labels = {l: i for i, l in enumerate(ship_labels)}

    def __call__(self, hypotheses):
        sizes = []
        
        for h in hypotheses:
            h_sizes = [0] * len(self.labels)
            for s in h.ships:
                h_sizes[self.labels[s.ship_label]] = s.size
            h_sizes = tuple(h_sizes)
            sizes.append(h_sizes)
        
        sizes_cnt = Counter(sizes)
        priors = np.array([1.0 / sizes_cnt[x] for x in sizes])
        return normalize(priors)