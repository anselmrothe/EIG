import numpy as np

def normalize(x):
    norm = sum(x)
    if norm == 0: return x
    else: return x / norm

class Bayes:
    def __init__(self, size):
        self.belief = self.prior(size)

    def __iter__(self):
        return self.belief.__iter__()

    def prior(self, size):
        # by default, this is a uniform distribution
        return np.ones(size) / size

    def update_belief(self, subset_ids):
        """
        Update belief about hypotheses given set of ids that is valid.
        Possibility of invalid hypotheses will be set to zero.
        """
        for id in subset_ids:
            self.belief[id] = 0
        self.belief = normalize(self.belief)

    def subset(self, subset_ids):
        """
        Get a subset of beliefs given ids.
        A generator is returned.
        """
        for id in subset_ids:
            yield self.belief[id]