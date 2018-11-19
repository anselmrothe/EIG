
class Context(object):
    """
    Class context is used for saving information about 
    observations, hypotheses, and beliefs.
    """
    def __init__(self, hypotheses, belief):
        self.hypotheses = hypotheses
        self.belief = belief
        self.valid_ids = list(range(len(hypotheses)))

    def observe(self, observation):
        valid_ids = self.hypotheses.observe(observation)
        self.belief.update_belief(valid_ids)
        self.valid_ids = valid_ids

    def get_answers(self, executor):
        return self.hypotheses.execute_on_subspace(executor, self.valid_ids), \
            self.belief.subset(self.valid_ids)
