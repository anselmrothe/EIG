import numpy as np

def normalize(x):
    norm = sum(x)
    if norm == 0: return x
    else: return x / norm

class Distribution:
    """
    Abstract class for Prior distributions
    """
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, hypotheses):
        raise NotImplementedError


class UniformDistribution(Distribution):
    def __init__(self):
        pass

    def __call__(self, hypotheses):
        size = len(hypotheses)
        return np.ones(size) / size


class Bayes:
    def __init__(self, hypotheses, prior_dist=None):
        if prior_dist is None:
            prior_dist = UniformDistribution()
        self.belief = prior_dist(hypotheses)

    def __iter__(self):
        return self.belief.__iter__()

    def update_belief(self, subset_ids):
        """
        Update belief about hypotheses given set of ids that is valid.
        Possibility of invalid hypotheses will be set to zero.
        """
        mask = np.zeros_like(self.belief)
        mask[subset_ids] = 1
        self.belief = normalize(self.belief * mask)

    def subset(self, subset_ids):
        """
        Get a subset of beliefs given ids.
        A generator is returned.
        """
        for id in subset_ids:
            yield self.belief[id]