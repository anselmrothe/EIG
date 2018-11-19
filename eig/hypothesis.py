
class HypothesisSpace:
    def __init__(self, *params, **kw_params):
        self.hypotheses = self.create_hypothesis_space(*params, **kw_params)

    def __len__(self):
        return len(self.hypotheses)

    def __iter__(self):
        return self.hypotheses.__iter__()

    def create_hypothesis_space(self, *params, **kw_params):
        """
        Given lists of parameters, return a list of hypotheses, 
        """
        raise NotImplementedError

    def observe(self, observation):
        """
        Given an observation, return a set of ids which hypothesis of that id 
        is consistent with the observation.
        """
        valid_ids = []
        for i in range(len(self.hypotheses)):
            if self.match(i, observation):
                valid_ids.append(i)
        return valid_ids

    def match(self, i, observation):
        """
        Test if a hypothesis is in consistent with the observation.
        Return True if it is, False elsewise.
        """
        raise NotImplementedError

    def execute_on_subspace(self, executor, subset_id):
        """
        Execute the executor on part of the hypothesis space given by the subset_id list.
        Return a list of answers.
        """
        raise NotImplementedError