
class HypothesesSpace:
    def __init__(self, *params, **kw_params):
        self.hypotheses = self.create_hypothesis_space(*params, **kw_params)

    def __len__(self):
        return len(self.hypotheses)

    def create_hypothesis_space(self, *params, **kw_params):
        """
        Given lists of parameters, return a list of hypotheses, 
        """
        raise NotImplementedError

    def observe(self, observation):
        """
        Given an observation, return a list of ids which hypothesis of that id 
        is not consistent with the observation.
        """
        invalid_ids = []
        for i in range(len(self.hypotheses)):
            if not self.match(i, observation):
                invalid_ids.append(i)
        return invalid_ids

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