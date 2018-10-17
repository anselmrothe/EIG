
class Context(object):
    """
    Class context is used for saving information about 
    observations, hypotheses, and beliefs.
    """
    def __init__(self, hypotheses, belief):
        self.hypotheses = hypotheses
        self.belief = belief

    def observe(self, observation):
        invalid_ids = self.hypotheses.observe(observation)
        self.belief.update_belief(invalid_ids)

    def hypotheses_subset(self):
        for h, p in zip(self.hypotheses, self.belief):
            if p > 0:
                yield h, p