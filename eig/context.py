
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

    def get_answers(self, executor):
        hypotheses_subset = []
        belief_subset = []
        for i, p in enumerate(self.belief):
            if p > 0:
                hypotheses_subset.append(i)
                belief_subset.append(p)
        return self.hypotheses.execute_on_subspace(executor, hypotheses_subset), belief_subset
